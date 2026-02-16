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

# API Routes
@app.get("/api/health")
async def health():
    return {"status": "healthy"}

@app.get("/api/classes")
async def get_classes(db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(CharacterClass))
    return result.scalars().all()

@app.get("/api/characters/{char_id}")
async def get_character(char_id: int, db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(Character).where(Character.id == char_id))
    char = result.scalar_one_or_none()
    if not char:
        raise HTTPException(status_code=404, detail="Character not found")
    return char

# Serve Frontend
frontend_path = os.path.join(os.getcwd(), "frontend/public")
if os.path.exists(frontend_path):
    app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")
