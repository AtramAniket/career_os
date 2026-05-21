from __future__ import annotations

from datetime import date, datetime, timezone
from enum import Enum
from typing import Optional

from sqlalchemy import ForeignKey, DateTime, Date, String, Text, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.extensions import db


class JobStatus(Enum):
    SAVED = "Saved"
    APPLIED = "Applied"
    ASSESSMENT = "Assessment"
    INTERVIEW = "Interview"
    OFFER = "Offer"
    REJECTED = "Rejected"
    GHOSTED = "Ghosted"


class WorkMode(Enum):
    REMOTE = "Remote"
    HYBRID = "Hybrid"
    ONSITE = "On-site"


class EmploymentType(Enum):
    FULL_TIME = "Full-time"
    PART_TIME = "Part-time"
    INTERNSHIP = "Internship"
    CONTRACT = "Contract"


class PriorityLevel(Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"


class JobApplication(db.Model):
    __tablename__ = "job_applications"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    company_name: Mapped[str] = mapped_column(
        db.String(150),
        nullable=False,
    )

    role_title: Mapped[str] = mapped_column(
        db.String(150),
        nullable=False,
    )

    job_url: Mapped[Optional[str]] = mapped_column(
        db.String(500),
        nullable=True,
    )

    location: Mapped[Optional[str]] = mapped_column(
        db.String(150),
        nullable=True,
    )

    work_mode: Mapped[Optional[WorkMode]] = mapped_column(
        db.Enum(WorkMode),
        nullable=True,
    )

    employment_type: Mapped[Optional[EmploymentType]] = mapped_column(
        db.Enum(EmploymentType),
        nullable=True,
    )

    salary_min: Mapped[Optional[int]] = mapped_column(
        nullable=True,
    )

    salary_max: Mapped[Optional[int]] = mapped_column(
        nullable=True,
    )

    source: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
    )

    status: Mapped[JobStatus] = mapped_column(
        db.Enum(JobStatus),
        default=JobStatus.SAVED,
        nullable=False,
        index=True,
    )

    priority: Mapped[PriorityLevel] = mapped_column(
        db.Enum(PriorityLevel),
        default=PriorityLevel.MEDIUM,
        nullable=False,
    )

    deadline: Mapped[Optional[date]] = mapped_column(
        Date,
        nullable=True,
    )

    date_saved: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    date_applied: Mapped[Optional[date]] = mapped_column(
        Date,
        nullable=True,
    )

    notes: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    user: Mapped["User"] = relationship(
        "User",
        back_populates="job_applications",
    )

    events: Mapped[list["ApplicationEvent"]] = relationship(
        "ApplicationEvent",
        back_populates="job_application",
        cascade="all, delete-orphan",
        lazy="select",
    )

    is_deleted: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        server_default="0"
    )

    deleted_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )