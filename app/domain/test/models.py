from sqlalchemy import (
    Boolean,
    Column,
    Integer,
    String,
    TIMESTAMP,
    func,
    JSON,
    ForeignKey,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

from app.db.base import Base
from app.domain.users.models import User


class MockTest(Base):
    __tablename__ = "mock_test"
    id = Column(Integer, primary_key=True)
    marks_scored = Column(Integer, default=0, nullable=True)
    test_status = Column(String(50), nullable=False)
    questions = Column(JSON, nullable=True)
    time_taken = Column(Integer, default=0, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)

    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    # Relationship to User (backref optional for bidirectional access)
    user = relationship("User", back_populates="test_results")


class TestSettings(Base):
    __tablename__ = "test_settings"

    id = Column(Integer, primary_key=True)
    key = Column(String, nullable=False)
    value = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)

    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )
