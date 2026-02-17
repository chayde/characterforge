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
    name: str
    level: int
    species_id: int
    class_id: int
    strength: int
    dexterity: int
    constitution: int
    intelligence: int
    wisdom: int
    charisma: int
    current_hp: int
    max_hp: int

    class Config:
        from_attributes = True
