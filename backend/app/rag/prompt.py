def build_rag_prompt(question: str, contexts: list[str]) -> str:
    context_text = "\n\n---\n\n".join(contexts)

    prompt = f"""Context:

{context_text}

---

Question:
{question}

请基于上面的 Context 回答。如果 Context 中没有相关信息，请如实说明。"""

    return prompt
