from datetime import datetime
from typing import List, Optional

from sqlalchemy import (
    Boolean,
    ForeignKey,
    Integer,
    String,
    Text,
    TIMESTAMP,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Question(Base):
    __tablename__ = "questions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    source: Mapped[str] = mapped_column(String(255), nullable=False)
    year: Mapped[str] = mapped_column(String(4), nullable=False)
    question_number: Mapped[str] = mapped_column(String(50), nullable=False)
    question_text: Mapped[str] = mapped_column(Text, nullable=False)
    has_diagram: Mapped[bool] = mapped_column(Boolean, default=False)
    diagram_description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    diagram_position: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    diagram_name: Mapped[str] = mapped_column(String(255), default="none")
    answer: Mapped[str] = mapped_column(String(50), nullable=False)
    solution: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    reviewed: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, server_default=func.current_timestamp()
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        server_default=func.current_timestamp(),
        onupdate=func.current_timestamp(),
    )

    # Relationship: one question has many options
    options: Mapped[List["Option"]] = relationship(
        "Option",
        back_populates="question",
        cascade="all, delete-orphan",  # Delete options if question is deleted
        lazy="selectin",  # Efficient loading of related options
    )

    def __repr__(self) -> str:
        return f"<Question {self.source} {self.year} {self.question_number}>"


class Option(Base):
    __tablename__ = "options"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    question_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("questions.id", ondelete="CASCADE"), nullable=False
    )
    label: Mapped[str] = mapped_column(String(50), nullable=False)  # A, B, C, D, etc.
    text: Mapped[str] = mapped_column(Text, nullable=False)
    option_has_diagram: Mapped[bool] = mapped_column(Boolean, default=False)
    option_diagram_description: Mapped[Optional[str]] = mapped_column(
        Text, nullable=True
    )
    option_diagram_name: Mapped[str] = mapped_column(String(255), default="none")

    # Relationship: many options belong to one question
    question: Mapped["Question"] = relationship("Question", back_populates="options")

    def __repr__(self) -> str:
        return f"<Option {self.label}: {self.text[:50]}...>"
