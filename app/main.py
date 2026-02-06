from datetime import datetime, timedelta
from typing import List
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
import os
import jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.database import create_tables, get_db
from app.repositories.project_repository import ProjectRepository
from app.repositories.task_repository import TaskRepository
from app.repositories.user_repository import UserRepository
from app.schemas.project import ProjectCreate, ProjectRead
from app.schemas.task import Task
from app.schemas.user import UserCreate, UserRead

SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "cD3s9bGxZ1q7Vt8PjKf4mYw2R0aH6nS",
)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 7

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_tables()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def _create_token(subject: str, expires_delta: timedelta) -> str:
    expire = datetime.utcnow() + expires_delta
    to_encode = {"exp": expire, "sub": subject}
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def create_access_token(subject: str, expires_delta: timedelta = None) -> str:
    expires = expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    return _create_token(subject, expires)


def create_refresh_token(subject: str) -> str:
    expires = timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    return _create_token(subject, expires)


async def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception
    user = UserRepository(db).get_by_email(email)
    if user is None:
        raise credentials_exception
    return user


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    refresh_token: str


@app.post("/auth/register", response_model=UserRead, status_code=201)
def register(user: UserCreate, db: Session = Depends(get_db)):
    repo = UserRepository(db)
    existing = repo.get_by_email(user.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed = get_password_hash(user.password)
    created = repo.create(
        email=user.email,
        password_hash=hashed,
        full_name=user.full_name,
    )
    return created


@app.post("/auth/login", response_model=TokenResponse)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    repo = UserRepository(db)
    user = repo.get_by_email(form_data.username)
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token(subject=user.email)
    refresh_token = create_refresh_token(subject=user.email)
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "refresh_token": refresh_token,
    }


@app.get("/users/me", response_model=UserRead)
def read_users_me(current_user=Depends(get_current_user)):
    return current_user


@app.post("/projects/", response_model=ProjectRead)
def create_project(
    project: ProjectCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    repo = ProjectRepository(db)
    with db.begin():
        created = repo.create(
            name=project.name,
            description=project.description,
            owner_id=current_user.id,
        )
    return created


@app.get("/projects/", response_model=List[ProjectRead])
def list_user_projects(
    db: Session = Depends(get_db), current_user=Depends(get_current_user)
):
    repo = ProjectRepository(db)
    all_projects = repo.list()
    user_projects = [
        p
        for p in all_projects
        if p.owner_id == current_user.id or current_user in p.members
    ]
    return user_projects


class MemberAdd(BaseModel):
    email: str


@app.post("/projects/{project_id}/members")
def add_project_member(
    project_id: int,
    payload: MemberAdd,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    project_repo = ProjectRepository(db)
    user_repo = UserRepository(db)
    project = project_repo.get(project_id)
    if project is None:
        raise HTTPException(status_code=404)
    if project.owner_id != current_user.id:
        raise HTTPException(status_code=403)
    member = user_repo.get_by_email(payload.email)
    if member is None:
        raise HTTPException(status_code=404)
    with db.begin():
        if member not in project.members:
            project.members.append(member)
            db.add(project)
    return {"status": "ok"}


@app.post("/projects/{project_id}/tasks", response_model=Task)
def create_task(
    project_id: int,
    task: Task,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    project_repo = ProjectRepository(db)
    task_repo = TaskRepository(db)
    project = project_repo.get(project_id)
    if project is None:
        raise HTTPException(status_code=404)
    if project.owner_id != current_user.id and current_user not in project.members:
        raise HTTPException(status_code=403)
    with db.begin():
        created = task_repo.create(
            title=task.title,
            description=task.description,
            project_id=project_id,
            assignee_id=task.assignee_id,
        )
    return created


@app.get("/projects/{project_id}/tasks", response_model=List[Task])
def list_project_tasks(
    project_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    project_repo = ProjectRepository(db)
    task_repo = TaskRepository(db)
    project = project_repo.get(project_id)
    if project is None:
        raise HTTPException(status_code=404)
    if project.owner_id != current_user.id and current_user not in project.members:
        raise HTTPException(status_code=403)
    tasks = [t for t in task_repo.list() if t.project_id == project_id]
    return tasks


class AssignPayload(BaseModel):
    assignee_id: int


@app.put("/tasks/{task_id}/assign")
def assign_task(
    task_id: int,
    payload: AssignPayload,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    task_repo = TaskRepository(db)
    project_repo = ProjectRepository(db)
    task = task_repo.get(task_id)
    if task is None:
        raise HTTPException(status_code=404)
    project = project_repo.get(task.project_id)
    if project.owner_id != current_user.id and current_user not in project.members:
        raise HTTPException(status_code=403)
    assignee = UserRepository(db).get(payload.assignee_id)
    if assignee is None:
        raise HTTPException(status_code=404)
    if assignee not in project.members and assignee.id != project.owner_id:
        raise HTTPException(status_code=400)
    with db.begin():
        task.assignee_id = assignee.id
        db.add(task)
        return {"status": "ok"}


class StatusPayload(BaseModel):
    status: str


@app.put("/tasks/{task_id}/status")
def update_task_status(
    task_id: int,
    payload: StatusPayload,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    task_repo = TaskRepository(db)
    project_repo = ProjectRepository(db)
    task = task_repo.get(task_id)
    if task is None:
        raise HTTPException(status_code=404)
    project = project_repo.get(task.project_id)
    if (
        project.owner_id != current_user.id
        and current_user not in project.members
        and task.assignee_id != current_user.id
    ):
        raise HTTPException(status_code=403)
    with db.begin():
        task.status = payload.status
        db.add(task)
    return {"status": "ok"}
