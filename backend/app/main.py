from fastapi import FastAPI, Depends, HTTPException
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from .database import init_db, get_session
from .models import Character, CharacterClass, Species, ClassLevel, Feature, User
from .schemas import CharacterCreate, CharacterResponse, UserCreate, UserResponse, Token
from .auth import get_password_hash, verify_password, create_access_token, get_current_user
from fastapi.security import OAuth2PasswordRequestForm
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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

# Auth Routes
@app.post("/api/register", response_model=UserResponse)
async def register(user_data: UserCreate, db: AsyncSession = Depends(get_session)):
    hashed_pwd = get_password_hash(user_data.password)
    new_user = User(username=user_data.username, email=user_data.email, hashed_password=hashed_pwd)
    db.add(new_user)
    try:
        await db.commit()
        await db.refresh(new_user)
        logger.info(f"New user registered: {new_user.username}")
        return new_user
    except Exception as e:
        logger.error(f"Error during registration: {str(e)}")
        if "UNIQUE" in str(e):
            if "username" in str(e):
                raise HTTPException(status_code=400, detail="Username already taken")
            if "email" in str(e):
                raise HTTPException(status_code=400, detail="Email already registered")
        raise HTTPException(status_code=400, detail=f"Registration failed: {str(e)}")

@app.post("/api/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(User).where(User.username == form_data.username))
    user = result.scalar_one_or_none()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

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
async def create_character(
    char_data: CharacterCreate, 
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    class_result = await db.execute(select(CharacterClass).where(CharacterClass.id == char_data.class_id))
    char_class = class_result.scalar_one_or_none()
    if not char_class:
        raise HTTPException(status_code=404, detail="Class not found")

    con_mod = (char_data.constitution - 10) // 2
    avg_die = (char_class.hit_die // 2) + 1
    max_hp = char_class.hit_die + con_mod + (char_data.level - 1) * (avg_die + con_mod)

    new_char = Character(
        **char_data.model_dump(),
        owner_id=current_user.id,
        max_hp=max_hp,
        current_hp=max_hp
    )
    db.add(new_char)
    await db.commit()
    await db.refresh(new_char)
    return new_char

@app.get("/api/characters", response_model=List[CharacterResponse])
async def list_characters(
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(select(Character).where(Character.owner_id == current_user.id))
    return result.scalars().all()

@app.delete("/api/characters/{char_id}")
async def delete_character(
    char_id: int,
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(select(Character).where(Character.id == char_id, Character.owner_id == current_user.id))
    char = result.scalar_one_or_none()
    if not char:
        raise HTTPException(status_code=404, detail="Character not found")
    
    await db.delete(char)
    await db.commit()
    return {"message": "Character deleted"}

@app.get("/api/characters/{char_id}", response_model=CharacterResponse)
async def get_character(
    char_id: int, 
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(select(Character).where(Character.id == char_id, Character.owner_id == current_user.id))
    char = result.scalar_one_or_none()
    if not char:
        raise HTTPException(status_code=404, detail="Character not found")
    return char

# Serve Frontend
frontend_path = os.path.join(os.getcwd(), "frontend/public")
if os.path.exists(frontend_path):
    app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")
