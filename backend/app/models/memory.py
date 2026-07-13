from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql import func

from app.core.database import Base


class UserProfile(Base):

    __tablename__ = "user_profiles"

    __table_args__ = {"extend_existing": True}

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), unique=True
    )

    target_job: Mapped[str] = mapped_column(
        String(200), default="", nullable=False
    )

    city: Mapped[str] = mapped_column(
        String(100), default="", nullable=False
    )

    salary: Mapped[str] = mapped_column(
        String(100), default="", nullable=False
    )

    education: Mapped[str] = mapped_column(
        String(200), default="", nullable=False
    )

    experience_years: Mapped[int] = mapped_column(default=0)

    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )


class UserPreference(Base):

    __tablename__ = "user_preferences"

    __table_args__ = {"extend_existing": True}

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    key: Mapped[str] = mapped_column(String(100), nullable=False)

    value: Mapped[str] = mapped_column(Text, default="", nullable=False)


class ExperienceRecord(Base):

    __tablename__ = "experience_records"

    __table_args__ = {"extend_existing": True}

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    event_type: Mapped[str] = mapped_column(
        String(50), nullable=False, default=""
    )

    version: Mapped[int] = mapped_column(default=1)

    accepted: Mapped[bool] = mapped_column(default=False)

    meta_json: Mapped[str] = mapped_column(Text, default="{}")

    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now()
    )
