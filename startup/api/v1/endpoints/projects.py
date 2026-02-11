from fastapi import APIRouter

router = APIRouter(prefix="/projects")


@router.post("/")
def create_project():
    return {"status": "created"}


@router.get("/")
def list_projects():
    return []
