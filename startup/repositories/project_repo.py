from sqlalchemy.orm import Session
from startup.models.project import Project


class ProjectRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, project_id: int):
        return self.db.query(Project).filter(Project.id == project_id).first()

    def create(self, name: str, description: str, owner_id: int):
        p = Project(name=name, description=description, owner_id=owner_id)
        self.db.add(p)
        self.db.flush()
        return p

    def list(self):
        return self.db.query(Project).all()
