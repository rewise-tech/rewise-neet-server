from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.domain.users import schemas
from app.domain.users.models import User
from app.domain.users.repository import UserRepository


class UserService:
    def __init__(self, session: Session) -> None:
        self.repo = UserRepository(session)

    def list_users(self) -> list[User]:
        return self.repo.list()

    def get_user(self, user_id: int) -> User | None:
        return self.repo.get(user_id)

    def create_user(self, payload: schemas.UserCreate) -> User:
        existing = self.repo.get_by_email(payload.email)
        if existing:
            raise ValueError("Email already registered")

        password_hash = hash_password(payload.password)
        return self.repo.create(
            name=payload.name,
            email=payload.email,
            mobile=payload.mobile,
            password_hash=password_hash,
            role=payload.role,
            is_active=payload.is_active,
        )

    def update_user(self, user: User, payload: schemas.UserUpdate) -> User:
        fields: dict[str, object] = {}
        if payload.name is not None:
            fields["name"] = payload.name
        if payload.mobile is not None:
            fields["mobile"] = payload.mobile
        if payload.role is not None:
            fields["role"] = payload.role
        if payload.is_active is not None:
            fields["is_active"] = payload.is_active
        if payload.password is not None:
            fields["password_hash"] = hash_password(payload.password)

        return self.repo.update(user, **fields)

    def delete_user(self, user: User) -> None:
        self.repo.delete(user)
