from .settings import settings


def get_database_url() -> str:
    return (
        f"postgresql+psycopg2://"
        f"{settings.DB_USER}:{settings.DB_PASSWORD}@"
        f"{settings.DB_HOST}:{settings.DB_PORT}/"
        f"{settings.DB_NAME}"
    )


def get_redis_url() -> str:
    return settings.REDIS_URL


def get_chroma_path() -> str:
    return settings.CHROMA_PATH
