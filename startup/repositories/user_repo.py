from sqlalchemy.orm import Session
from startup.models.user import User


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, user_id: int):
        return self.db.query(User).filter(User.id == user_id).first()

    def get_by_email(self, email: str):
        return self.db.query(User).filter(User.email == email).first()

    def create(self, email: str, password_hash: str, full_name: str = None):
        user = User(email=email, password_hash=password_hash, full_name=full_name)
        self.db.add(user)
        self.db.flush()
        return user

    def list(self):
        return self.db.query(User).all()
