from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, TIMESTAMP, func
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime

from app.db.base import Base


class Subject(Base):
    __tablename__ = "subjects"

    id = Column(Integer, primary_key=True)
    subject_name = Column(String, nullable=False)
    no_of_questions = Column(Integer, nullable=True)
    is_active = Column(Boolean, default=True)

    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, server_default=func.current_timestamp()
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        server_default=func.current_timestamp(),
        onupdate=func.current_timestamp(),
    )

    chapters = relationship(
        "Chapter", back_populates="subject", cascade="all, delete-orphan"
    )


class Chapter(Base):
    __tablename__ = "chapters"

    id = Column(Integer, primary_key=True)
    no = Column(String, nullable=False)
    name = Column(String, nullable=False)
    formatted_name = Column(String, nullable=False)
    no_of_questions = Column(Integer, nullable=True)
    is_active = Column(Boolean, default=True)

    subject_id = Column(
        Integer, ForeignKey("subjects.id", ondelete="CASCADE"), nullable=False
    )
    subject = relationship("Subject", back_populates="chapters")

    topics = relationship(
        "Topic", back_populates="chapter", cascade="all, delete-orphan"
    )


class Topic(Base):
    __tablename__ = "topics"

    id = Column(Integer, primary_key=True)
    no = Column(String, nullable=False)
    name = Column(String, nullable=False)
    formatted_name = Column(String, nullable=False)
    no_of_questions = Column(Integer, nullable=True)
    is_active = Column(Boolean, default=True)

    chapter_id = Column(
        Integer, ForeignKey("chapters.id", ondelete="CASCADE"), nullable=False
    )
    chapter = relationship("Chapter", back_populates="topics")
