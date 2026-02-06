from app.repositories.user_repository import UserRepository


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def register_user(self, username: str, email: str):
        return self.user_repository.create_user(username, email)

    def get_user_info(self, user_id: int):
        return self.user_repository.get_user(user_id)
