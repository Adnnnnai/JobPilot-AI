from .settings import settings


def get_llm_config() -> dict:
    return {
        "api_key": settings.LLM_API_KEY,
        "base_url": settings.LLM_BASE_URL,
        "model": settings.MODEL_NAME,
    }
