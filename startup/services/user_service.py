from startup.repositories.user_repo import UserRepository
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService:
    def __init__(self, db):
        self.repo = UserRepository(db)

    def create_user(self, email: str, password: str, full_name: str = None):
        hashed = pwd_context.hash(password)
        return self.repo.create(email=email, password_hash=hashed, full_name=full_name)

    def get_by_email(self, email: str):
        return self.repo.get_by_email(email)
