from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from .database import init_db, get_session
from .models import Character, CharacterClass, Species, ClassLevel, Feature
import os

app = FastAPI(title="CharacterForge API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def on_startup():
    await init_db()

from .schemas import CharacterCreate, CharacterResponse

# API Routes
@app.get("/api/health")
async def health():
    return {"status": "healthy"}

@app.get("/api/classes")
async def get_classes(db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(CharacterClass))
    return result.scalars().all()

@app.get("/api/species")
async def get_species(db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(Species))
    return result.scalars().all()

@app.post("/api/characters", response_model=CharacterResponse)
async def create_character(char_data: CharacterCreate, db: AsyncSession = Depends(get_session)):
    # Fetch class to get hit die
    class_result = await db.execute(select(CharacterClass).where(CharacterClass.id == char_data.class_id))
    char_class = class_result.scalar_one_or_none()
    if not char_class:
        raise HTTPException(status_code=404, detail="Class not found")

    # Basic HP Calculation: Hit Die + Con Modifier + (Level-1)*(Avg Hit Die + Con Modifier)
    con_mod = (char_data.constitution - 10) // 2
    avg_die = (char_class.hit_die // 2) + 1
    max_hp = char_class.hit_die + con_mod + (char_data.level - 1) * (avg_die + con_mod)

    new_char = Character(
        **char_data.model_dump(),
        max_hp=max_hp,
        current_hp=max_hp
    )
    db.add(new_char)
    await db.commit()
    await db.refresh(new_char)
    return new_char

@app.get("/api/characters/{char_id}", response_model=CharacterResponse)

# Serve Frontend
frontend_path = os.path.join(os.getcwd(), "frontend/public")
if os.path.exists(frontend_path):
    app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")
