import aioredis
from aioredis.client import Redis

from app.configs import Settings


async def create_cache() -> Redis:
    redis = await aioredis.from_url(
        f'redis://@{Settings().redis_host}:{Settings().redis_port}'
    )
    return redis
