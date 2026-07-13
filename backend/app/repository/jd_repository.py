from sqlalchemy.orm import Session

from app.models.job_description import JobDescription


class JDRepository:

    @staticmethod
    def create(db: Session, jd: JobDescription) -> JobDescription:
        db.add(jd)
        db.commit()
        db.refresh(jd)
        return jd

    @staticmethod
    def list_all(db: Session, limit: int = 50):
        return (
            db.query(JobDescription)
            .order_by(JobDescription.created_at.desc())
            .limit(limit)
            .all()
        )

    @staticmethod
    def search(db: Session, keyword: str, limit: int = 20):
        return (
            db.query(JobDescription)
            .filter(
                JobDescription.keywords.ilike(f"%{keyword}%")
                | JobDescription.title.ilike(f"%{keyword}%")
            )
            .order_by(JobDescription.created_at.desc())
            .limit(limit)
            .all()
        )
