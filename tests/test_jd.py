"""
测试核心工具: JD搜索、生成、提取、写入
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "agent"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))


def test_jd_generator():
    from app.services.jd_generator import JDGenerator
    jd = JDGenerator.generate("Python开发工程师")
    assert "title" in jd
    assert "tech_stack" in jd
    assert len(jd["tech_stack"]) >= 3
    assert "requirements" in jd
    assert len(jd["requirements"]) >= 3


def test_jd_writer():
    from app.services.jd_writer import JDWriter
    from app.core.database import SessionLocal
    from app.models.job_description import JobDescription
    jd = {
        "title": "测试岗位",
        "company": "测试公司",
        "salary": "20k",
        "city": "深圳",
        "tech_stack": ["Python", "FastAPI"],
        "requirements": ["会写代码"],
        "description": "测试用JD",
        "keywords": "测试",
        "source": "test",
    }
    JDWriter.save(jd)
    db = SessionLocal()
    record = db.query(JobDescription).filter(JobDescription.title == "测试岗位").first()
    assert record is not None
    assert record.company == "测试公司"
    db.delete(record)
    db.commit()
    db.close()


def test_jd_extractor():
    from app.services.jd_extractor import JDExtractor
    html = "AI Agent开发工程师\n公司: XX科技\n薪资: 30-50K\n要求: Python, LangGraph, FastAPI"
    jd = JDExtractor.extract(html)
    assert "title" in jd or "description" in jd
