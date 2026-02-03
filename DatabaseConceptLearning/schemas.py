
from pydantic import BaseModel
from typing import List, Optional

class TaskSchema(BaseModel):
    id: Optional[int]
    title: str
    class Config:
        orm_mode = True

class ProjectSchema(BaseModel):
    id: Optional[int]
    name: str
    tasks: List[TaskSchema] = []
    class Config:
        orm_mode = True

class UserSchema(BaseModel):
    id: Optional[int]
    username: str
    email: str
    projects: List[ProjectSchema] = []
    class Config:
        orm_mode = True
