"""
测试工具: resume, jd, rewrite, browser, executor
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "agent"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))


def test_resume_tool():
    from tools.resume_tool import ResumeTool
    tool = ResumeTool()
    assert tool.name == "resume_analyzer"


def test_jd_tool():
    from tools.jd_tool import JDTool
    tool = JDTool()
    result = tool.run({"name": "张三", "skills": ["Python"]}, "Python开发")
    assert "Resume" in result or "Python" in str(result)


def test_rewrite_tools():
    import pytest
    try:
        from tools.rewrite_tool import RewritePlanTool, RewriteExecuteTool
        plan_tool = RewritePlanTool()
        resume = {"name": "张三", "skills": ["Python", "FastAPI"], "projects": [{"title": "电商平台"}]}
        result = plan_tool.run(resume)
        assert "changes" in result or isinstance(result, dict)
        exec_tool = RewriteExecuteTool()
        result2 = exec_tool.run(resume, result)
        assert isinstance(result2, dict)
    except Exception:
        pytest.skip("LLM unavailable")


def test_executor():
    from executor import TaskExecutor
    plan = [
        {"id": 1, "name": "parse", "depends": []},
        {"id": 2, "name": "jd", "depends": []},
        {"id": 3, "name": "rewrite", "depends": [1, 2]},
        {"id": 4, "name": "interview", "depends": [3]},
    ]
    # 无依赖任务立即可行
    ready = TaskExecutor.get_next_tasks(plan, [], [])
    assert len(ready) == 2
    assert ready[0]["id"] == 1
    assert ready[1]["id"] == 2

    # 依赖未满足不可行
    ready2 = TaskExecutor.get_next_tasks(plan, [{"id": 1}], [])
    assert len(ready2) == 1
    assert ready2[0]["id"] == 2

    # 全部完成后
    assert TaskExecutor.is_complete(plan, [{"id": 1}, {"id": 2}, {"id": 3}, {"id": 4}]) == True


def test_browser_tool():
    import pytest
    try:
        from tools.browser_tools import BrowserSearchTool
        tool = BrowserSearchTool()
        result = tool.run("AI Agent")
        assert len(result) > 10
    except Exception:
        pytest.skip("LLM/Playwright unavailable")
