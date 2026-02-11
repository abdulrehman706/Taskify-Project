from startup.repositories.project_repo import ProjectRepository


class ProjectService:
    def __init__(self, db):
        self.repo = ProjectRepository(db)

    def create_project(self, name: str, description: str, owner_id: int):
        return self.repo.create(name=name, description=description, owner_id=owner_id)

    def list(self):
        return self.repo.list()
