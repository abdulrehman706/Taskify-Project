from fastapi import APIRouter

router = APIRouter(prefix="/tasks")


@router.post("/")
def create_task():
    return {"status": "created"}


@router.put("/{task_id}/assign")
def assign_task(task_id: int):
    return {"status": "assigned", "task_id": task_id}
