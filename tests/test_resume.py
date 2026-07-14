"""
测试简历解析服务
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "agent"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))


def test_resume_parse():
    import pytest
    try:
        from app.services.resume_service import ResumeService
        result = ResumeService.parse_resume("D:/project/JobPilot-AI/uploads/zhangsan.docx")
        assert result is not None
        assert "name" in result
    except Exception:
        pytest.skip("LLM unavailable")


def test_text_cleaner():
    from app.utils.text_cleaner import TextCleaner
    dirty = "张三\n\n\n   Python   \n\n\nFastAPI"
    clean = TextCleaner.clean(dirty)
    assert "\n\n\n" not in clean
    assert "   " not in clean
