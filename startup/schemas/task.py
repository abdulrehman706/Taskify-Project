from pydantic import BaseModel
from typing import Optional


class TaskCreate(BaseModel):
    title: str
    description: Optional[str]
    assignee_id: Optional[int]


class TaskRead(BaseModel):
    id: int
    title: str
    description: Optional[str]
    project_id: int
    assignee_id: Optional[int]
    status: str

    class Config:
        orm_mode = True
