"""
JD Writer

每个采集的岗位 → 立即保存到 PostgreSQL
"""
from app.core.database import SessionLocal
from app.models.job_description import JobDescription
from app.repository.jd_repository import JDRepository


class JDWriter:

    @staticmethod
    def save(jd: dict):
        db = SessionLocal()
        try:
            record = JobDescription(
                title=jd.get("title", ""),
                company=jd.get("company", ""),
                salary=jd.get("salary", ""),
                city=jd.get("city", jd.get("location", "")),
                tech_stack=", ".join(jd.get("tech_stack", [])),
                requirements="\n".join(jd.get("requirements", [])),
                content=jd.get("description", ""),
                keywords=jd.get("keywords", ""),
                source=jd.get("source", "unknown"),
            )
            JDRepository.create(db, record)
        finally:
            db.close()

    @staticmethod
    def search(keyword: str, limit: int = 20):
        db = SessionLocal()
        try:
            records = JDRepository.search(db, keyword, limit=limit)
            return [{
                "title": r.title,
                "company": r.company,
                "salary": r.salary,
                "city": r.city,
                "tech_stack": r.tech_stack,
                "requirements": r.requirements,
                "source": r.source,
            } for r in records]
        finally:
            db.close()
