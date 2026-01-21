from __future__ import annotations

from sqlalchemy import Boolean, Column, Integer, String, TIMESTAMP, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    mobile = Column(String(32), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(64), nullable=False, server_default="user")
    is_active = Column(Boolean, default=True)

    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    mock_tests = relationship("MockTest", back_populates="user")

    def __repr__(self) -> str:
        return f"<User {self.name} {self.email} {self.mobile}>"
