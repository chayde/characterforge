import asyncio
from backend.app.database import engine, Base, async_session
from backend.app.models import Feature, Species, CharacterClass, ClassLevel

async def seed():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async with async_session() as session:
        # 1. Add Species
        human = Species(name="Human", description="Versatile and ambitious.", speed=30, size="Medium")
        session.add(human)
        
        # 2. Add Fighter Class
        fighter = CharacterClass(name="Fighter", hit_die=10, primary_ability="Strength/Dexterity")
        session.add(fighter)
        await session.flush()
        
        # 3. Add Features
        second_wind = Feature(
            name="Second Wind",
            description="You have a limited well of stamina that you can draw on to protect yourself from harm.",
            source="SRD 2024",
            type="bonus_action",
            mechanics={"healing": "1d10 + level"}
        )
        action_surge = Feature(
            name="Action Surge",
            description="You can push yourself beyond your normal limits for a moment. On your turn, you can take one additional action.",
            source="SRD 2024",
            type="action",
            mechanics={"extra_action": 1}
        )
        session.add_all([second_wind, action_surge])
        
        # 4. Add Class Levels (1-5)
        for lvl in range(1, 6):
            prof_bonus = 2 if lvl < 5 else 3
            cl = ClassLevel(
                class_id=fighter.id,
                level=lvl,
                proficiency_bonus=prof_bonus,
                features_desc=f"Fighter Level {lvl} features"
            )
            session.add(cl)
            
        await session.commit()
        print("Database seeded with Fighter 1-5 SRD data!")

if __name__ == "__main__":
    asyncio.run(seed())
