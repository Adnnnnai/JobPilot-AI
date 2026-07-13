"""Cache Manager: 统一缓存入口，当前使用内存缓存（后续可切换 Redis）"""
from .redis_cache import get_cache
from .cache_key import CacheKey


class CacheManager:
    @staticmethod
    def get_llm_response(prompt: str, model: str):
        return get_cache().get(CacheKey.llm(prompt, model))

    @staticmethod
    def set_llm_response(prompt: str, model: str, response: str, ttl: int = 600):
        get_cache().set(CacheKey.llm(prompt, model), response, ttl)

    @staticmethod
    def get_resume(resume_id: int):
        return get_cache().get(CacheKey.resume(resume_id))

    @staticmethod
    def set_resume(resume_id: int, data: str, ttl: int = 3600):
        get_cache().set(CacheKey.resume(resume_id), data, ttl)

    @staticmethod
    def get_jd(keyword: str):
        return get_cache().get(CacheKey.jd(keyword))

    @staticmethod
    def set_jd(keyword: str, data: str, ttl: int = 1800):
        get_cache().set(CacheKey.jd(keyword), data, ttl)
