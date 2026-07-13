from .base_tool import BaseTool

from app.rag.knowledge.resume_kb import ResumeKB
from app.rag.knowledge.jd_kb import JDKB
from app.rag.knowledge.interview_kb import InterviewKB


class ResumeRAGTool(BaseTool):

    name = "resume_rag"
    description = "搜索简历库：项目经历、技能、教育背景"

    def run(self, query: str):
        results = ResumeKB.search(query, n_results=3)
        return results.get("documents", [[]])[0]


class JDRAGTool(BaseTool):

    name = "jd_rag"
    description = "搜索岗位库：岗位要求、技术栈、职责"

    def run(self, query: str):
        results = JDKB.search(query, n_results=3)
        return results.get("documents", [[]])[0]


class InterviewRAGTool(BaseTool):

    name = "interview_rag"
    description = "搜索面试题库：面试题、答案"

    def run(self, query: str):
        results = InterviewKB.search(query, n_results=3)
        return results.get("documents", [[]])[0]
