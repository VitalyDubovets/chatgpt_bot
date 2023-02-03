from contextvars import ContextVar

from aioredis import Redis, from_url

from src.infrstructure.config import settings

redis_connection: Redis = from_url(settings.REDIS_URI)

redis: ContextVar[Redis] = ContextVar("redis")

redis.set(redis_connection)
