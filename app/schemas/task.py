from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Task(BaseModel):
    id: Optional[int] = None
    title: str
    description: Optional[str] = None
    project_id: Optional[int] = None
    assignee_id: Optional[int] = None
    status: Optional[str] = "open"
    created_at: Optional[datetime] = None

    class Config:
        orm_mode = True
