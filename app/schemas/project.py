from datetime import datetime
from typing import Optional

from pydantic import BaseModel


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
