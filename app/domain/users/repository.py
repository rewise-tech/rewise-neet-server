from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domain.users.models import User


class UserRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def list(self) -> list[User]:
        stmt = select(User).order_by(User.id)
        return list(self.session.scalars(stmt))

    def get(self, user_id: int) -> Optional[User]:
        return self.session.get(User, user_id)

    def get_by_email(self, email: str) -> Optional[User]:
        stmt = select(User).where(User.email == email)
        return self.session.scalars(stmt).first()

    def create(
        self,
        *,
        name: str,
        email: str,
        mobile: str,
        password_hash: str,
        role: str,
        is_active: bool,
    ) -> User:
        user = User(
            name=name,
            email=email,
            mobile=mobile,
            password_hash=password_hash,
            role=role,
            is_active=is_active,
        )
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def update(self, user: User, **fields) -> User:
        for key, value in fields.items():
            if value is not None:
                setattr(user, key, value)
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def delete(self, user: User) -> None:
        self.session.delete(user)
        self.session.commit()
