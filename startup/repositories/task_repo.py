from sqlalchemy.orm import Session
from startup.models.task import Task


class TaskRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, task_id: int):
        return self.db.query(Task).filter(Task.id == task_id).first()

    def create(
        self,
        title: str,
        description: str,
        project_id: int,
        assignee_id: int = None,
    ):
        t = Task(
            title=title,
            description=description,
            project_id=project_id,
            assignee_id=assignee_id,
        )
        self.db.add(t)
        self.db.flush()
        return t

    def list(self):
        return self.db.query(Task).all()
