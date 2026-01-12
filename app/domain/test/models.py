from sqlalchemy import Boolean, Column, Integer, String, TIMESTAMP, func
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

from app.db.base import Base


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
