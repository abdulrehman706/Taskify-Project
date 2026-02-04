from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ProjectCreate(BaseModel):
    name: str
    description: Optional[str]
    owner_id: int

class ProjectRead(BaseModel):
    id: int
    name: str
    description: Optional[str]
    owner_id: int
    created_at: Optional[datetime]
    class Config:
        orm_mode = True
