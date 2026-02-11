from startup.repositories.task_repo import TaskRepository


class TaskService:
    def __init__(self, db):
        self.repo = TaskRepository(db)

    def create_task(
        self,
        title: str,
        description: str,
        project_id: int,
        assignee_id: int = None,
    ):
        return self.repo.create(
            title=title,
            description=description,
            project_id=project_id,
            assignee_id=assignee_id,
        )

    def list(self):
        return self.repo.list()
