from .settings import settings


def get_redis_config() -> dict:
    return {"url": settings.REDIS_URL}
