from fastapi import APIRouter
from startup.api.v1.endpoints import health, auth, users, projects, tasks, notifications

api_router = APIRouter()


v1 = APIRouter(prefix="/api/v1")
v1.include_router(health.router)
v1.include_router(auth.router)
v1.include_router(users.router)
v1.include_router(projects.router)
v1.include_router(tasks.router)
v1.include_router(notifications.router)

api_router.include_router(v1)
