from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.core.database import Base


class Resume(Base):

    __tablename__ = "resumes"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id")
    )

    filename: Mapped[str] = mapped_column(
        String(255)
    )

    filepath: Mapped[str] = mapped_column(
        String(500)
    )

    status: Mapped[str] = mapped_column(
        String(20),
        default="uploaded"
    )
