class CacheKey:
    @staticmethod
    def llm(prompt: str, model: str) -> str:
        import hashlib
        raw = f"{model}:{prompt}"
        return hashlib.sha256(raw.encode()).hexdigest()[:32]

    @staticmethod
    def resume(resume_id: int) -> str:
        return f"resume:{resume_id}"

    @staticmethod
    def jd(keyword: str) -> str:
        return f"jd:{keyword}"
