from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.task import Task

class TaskRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, task_id: int) -> Optional[Task]:
        return self.db.query(Task).filter(Task.id == task_id).first()

    def list(self, skip: int = 0, limit: int = 100) -> List[Task]:
        return self.db.query(Task).offset(skip).limit(limit).all()

    def create(self, title: str, description: Optional[str], project_id: int, assignee_id: Optional[int]) -> Task:
        task = Task(title=title, description=description, project_id=project_id, assignee_id=assignee_id)
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task

    def delete(self, task_id: int) -> None:
        obj = self.get(task_id)
        if obj:
            self.db.delete(obj)
            self.db.commit()
