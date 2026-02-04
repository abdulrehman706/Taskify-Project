from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.project import Project

class ProjectRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, project_id: int) -> Optional[Project]:
        return self.db.query(Project).filter(Project.id == project_id).first()

    def list(self, skip: int = 0, limit: int = 100) -> List[Project]:
        return self.db.query(Project).offset(skip).limit(limit).all()

    def create(self, name: str, description: Optional[str], owner_id: int) -> Project:
        project = Project(name=name, description=description, owner_id=owner_id)
        self.db.add(project)
        self.db.commit()
        self.db.refresh(project)
        return project

    def delete(self, project_id: int) -> None:
        obj = self.get(project_id)
        if obj:
            self.db.delete(obj)
            self.db.commit()
