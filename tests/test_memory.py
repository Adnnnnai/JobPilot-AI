"""
测试 Memory: Profile, Preferences, Experience, Strategy
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "agent"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))


def test_profile():
    from app.core.database import SessionLocal
    from app.services.memory_service import MemoryService
    db = SessionLocal()
    MemoryService.save_profile(db, 1, target_job="AI Agent", city="深圳", salary="20k", education="本科", experience_years=3)
    profile = MemoryService.get_profile(db, 1)
    assert profile["target_job"] == "AI Agent" or profile["target_job"] == "test"
    db.close()


def test_preferences():
    from app.core.database import SessionLocal
    from app.services.memory_service import MemoryService
    db = SessionLocal()
    MemoryService.set_preference(db, 1, "test_key", "test_value")
    prefs = MemoryService.get_preferences(db, 1)
    assert "test_key" in prefs
    db.close()


def test_experience():
    from app.core.database import SessionLocal
    from app.services.memory_service import MemoryService
    db = SessionLocal()
    MemoryService.record_experience(db, 1, "test_event", version=1, accepted=True, meta={"note": "单元测试"})
    versions = MemoryService.get_accepted_versions(db, 1, "test_event")
    assert len(versions) >= 1
    db.close()


def test_strategy():
    from memory.strategy import MemoryStrategy
    assert MemoryStrategy.should_save("帮我优化简历") == True
    assert MemoryStrategy.should_save("你好") == False
    assert MemoryStrategy.should_save("不要Java") == True
    assert MemoryStrategy.should_save("天气不错") == False

    prefs = MemoryStrategy.extract_preferences("不要Java")
    assert prefs.get("avoid_skill") == "Java"

    prefs2 = MemoryStrategy.extract_preferences("我想远程办公")
    assert prefs2.get("work_mode") == "remote"
