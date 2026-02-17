from sqlalchemy import Column, Integer, String, ForeignKey, Text, JSON, Table
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

# Many-to-many table for features (e.g., a Fighter level might grant multiple features)
feature_association = Table(
    'feature_association',
    Base.metadata,
    Column('feature_id', Integer, ForeignKey('features.id')),
    Column('owner_id', Integer), # ID of Class, Species, or Level
    Column('owner_type', String) # 'class', 'species', 'level', 'subclass'
)

class Feature(Base):
    __tablename__ = "features"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text)
    source = Column(String) # e.g., "SRD 2024", "PHB 2024"
    type = Column(String) # "passive", "action", "bonus_action", "reaction"
    mechanics = Column(JSON) # Store logic like {"bonus": {"strength": 2}} or {"action": "Second Wind"}

class Species(Base):
    __tablename__ = "species"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text)
    speed = Column(Integer, default=30)
    size = Column(String, default="Medium")

class CharacterClass(Base):
    __tablename__ = "classes"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    hit_die = Column(Integer) # e.g., 10 for Fighter
    primary_ability = Column(String) # e.g., "Strength"

class ClassLevel(Base):
    __tablename__ = "class_levels"
    id = Column(Integer, primary_key=True, index=True)
    class_id = Column(Integer, ForeignKey("classes.id"))
    level = Column(Integer)
    proficiency_bonus = Column(Integer)
    features_desc = Column(Text) # Summary text

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    email = Column(String, unique=True, index=True)

class Character(Base):
    __tablename__ = "characters"
    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String, index=True)
    level = Column(Integer, default=1)
    species_id = Column(Integer, ForeignKey("species.id"))
    class_id = Column(Integer, ForeignKey("classes.id"))
    
    # Ability Scores
    strength = Column(Integer, default=10)
    dexterity = Column(Integer, default=10)
    constitution = Column(Integer, default=10)
    intelligence = Column(Integer, default=10)
    wisdom = Column(Integer, default=10)
    charisma = Column(Integer, default=10)
    
    current_hp = Column(Integer)
    max_hp = Column(Integer)
    temp_hp = Column(Integer, default=0)
    
    # JSON field for equipment, spells known, etc.
    inventory = Column(JSON, default=list)
    spells = Column(JSON, default=list)
    resources = Column(JSON, default=dict) # e.g., {"second_wind": {"current": 1, "max": 1}}
