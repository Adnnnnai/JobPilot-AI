from .base_tool import BaseTool

from app.rag.retriever import search_resumes
from app.rag.prompt import build_rag_prompt


class RetrieverTool(BaseTool):

    name = "resume_search"

    description = "Search resume knowledge base"

    def run(self, query: str, n_results: int = 3):
        results = search_resumes(query, n_results=n_results)
        contexts = results.get("documents", [[]])[0]
        return build_rag_prompt(query, contexts)
