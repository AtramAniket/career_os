from __future__ import annotations

from typing import Optional
from datetime import datetime, timezone

from sqlalchemy import Text, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.extensions import db


class MockInterviewQuestion(db.Model):
    __tablename__ = "mock_interview_questions"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    session_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("mock_interview_sessions.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )

    question: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    category: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="resume",
    )

    display_order: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    mock_interview_session: Mapped["MockInterviewSession"] = relationship(
        "MockInterviewSession",
        back_populates="mock_interview_questions",
    )

    mock_interview_responses: Mapped[list["MockInterviewResponse"]] = relationship(
        "MockInterviewResponse",
        back_populates="question",
        cascade="all, delete-orphan",
    )