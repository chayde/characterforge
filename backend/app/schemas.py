from pydantic import BaseModel
from typing import List, Optional, Dict

class CharacterCreate(BaseModel):
    name: str
    species_id: int
    class_id: int
    level: int = 1
    strength: int = 10
    dexterity: int = 10
    constitution: int = 10
    intelligence: int = 10
    wisdom: int = 10
    charisma: int = 10

class CharacterResponse(BaseModel):
    id: int
    owner_id: Optional[int]
    name: str
    level: int
    # ... rest of fields

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
