from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    Integer,
    String,
    Text,
    TIMESTAMP,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

from app.db.base import Base


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)

    # Main fields from the root JSON
    source = Column(String, nullable=True, index=True)
    year = Column(String, nullable=True, index=True)
    subject = Column(String, nullable=True, index=True)
    chapter = Column(String, nullable=True, index=True)
    topic = Column(String, nullable=True, index=True)
    question_number = Column(String, nullable=False, index=True)
    question_text = Column(Text, nullable=True)
    difficulty = Column(String, nullable=True)
    has_diagram = Column(Boolean, default=False)
    diagram_description = Column(Text)
    diagram_position = Column(String)
    diagram_name = Column(Text)
    answer = Column(String, nullable=True)
    ai_answer = Column(String, nullable=True)
    solution = Column(Text)
    reviewed = Column(Boolean, default=False)

    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, server_default=func.current_timestamp()
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        server_default=func.current_timestamp(),
        onupdate=func.current_timestamp(),
    )

    # Relationship to options
    options = relationship(
        "Option", back_populates="question", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Question {self.source} {self.year} #{self.question_number}>"


class Option(Base):
    __tablename__ = "options"

    id = Column(Integer, primary_key=True, index=True)

    # Foreign key to parent question
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)

    label = Column(String, nullable=True)
    text = Column(Text, nullable=True)

    has_diagram = Column(Boolean, default=False)
    diagram_description = Column(Text)
    diagram_name = Column(Text)

    # Relationship back to question
    question = relationship("Question", back_populates="options")

    def __repr__(self):
        return f"<Option {self.label}: {self.text[:50]}...>"
