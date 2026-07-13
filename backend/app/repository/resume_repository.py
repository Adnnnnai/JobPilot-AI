from sqlalchemy.orm import Session

from app.models.resume import Resume


class ResumeRepository:

    @staticmethod
    def get_by_id(
        db: Session,
        resume_id: int
    ):
        return (
            db.query(Resume)
            .filter(Resume.id == resume_id)
            .first()
        )

    @staticmethod
    def update(
        db: Session,
        resume: Resume
    ):
        db.commit()
        db.refresh(resume)
        return resume

    @staticmethod
    def create(
        db: Session,
        resume: Resume
    ):

        db.add(resume)

        db.commit()

        db.refresh(resume)

        return resume
