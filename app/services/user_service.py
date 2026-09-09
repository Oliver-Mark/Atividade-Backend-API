from app.core.exceptions import ConflictException, EntityNotFoundException
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserUpdate


class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def list_users(self, skip: int = 0, limit: int = 100) -> list[User]:
        return self.user_repo.get_all(skip=skip, limit=limit)

    def get_user_by_id(self, user_id: int) -> User:
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise EntityNotFoundException("User not found")
        return user

    def create_user(self, data: UserCreate) -> User:
        existing_user = self.user_repo.get_by_email(data.email)
        if existing_user:
            raise ConflictException("Email already registered")
        return self.user_repo.create(name=data.name, email=data.email)

    def update_user(self, user_id: int, data: UserUpdate) -> User:
        user = self.get_user_by_id(user_id)

        if data.email and data.email != user.email:
            existing_email = self.user_repo.get_by_email(data.email)
            if existing_email:
                raise ConflictException("Email already registered")

        return self.user_repo.update(
            user=user,
            name=data.name,
            email=data.email,
        )

    def delete_user(self, user_id: int) -> None:
        user = self.get_user_by_id(user_id)
        self.user_repo.delete(user)

    def get_user_courses(self, user_id: int) -> User:
        user = self.user_repo.get_with_courses(user_id)
        if not user:
            raise EntityNotFoundException("User not found")
        return user
