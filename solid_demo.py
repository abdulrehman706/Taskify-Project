from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from DatabaseConceptLearning.db import Base, engine, SessionLocal
from DatabaseConceptLearning.models import User
from DatabaseConceptLearning.repository import UserRepository
from DatabaseConceptLearning.service import UserService
from DatabaseConceptLearning.schemas import UserSchema

app = FastAPI(title="TaskFlow Pro SOLID Demo")

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_user_service(db: Session = Depends(get_db)):
    user_repo = UserRepository(db)
    return UserService(user_repo)

@app.post("/users/", response_model=UserSchema)
def register_user(user: UserSchema, user_service: UserService = Depends(get_user_service)):
    db_user = user_service.register_user(user.username, user.email)
    return db_user

@app.get("/users/", response_model=list[UserSchema])
def list_users(db: Session = Depends(get_db)):
    return db.query(User).all()

@app.get("/ping")
def ping():
    return {"message": "API is up!"}
