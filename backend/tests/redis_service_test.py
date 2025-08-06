import time
import datetime
import pytest
import asyncio

from backend.src.services.redis_service import RedisService


# @pytest.fixture
async def seeded_redis():
    print(time.time())
    redis_service: RedisService = RedisService()
    await redis_service.r.flushall()
    _, top, left = await redis_service.create_snake('maxim', 'some_sid')
    await redis_service.r.hset('apple:1', mapping={
        'left': left,
        'top': top - 20,
    })
    await redis_service.r.hset('apple:2', mapping={
        'left': left,
        'top': top - 40,
    })
    await redis_service.r.hset('apple:3', mapping={
        'left': left,
        'top': top - 60,
    })
    await redis_service.move()
    await redis_service.move()
    await redis_service.move()
    await redis_service.change_direction('some_sid', 'right')
    await redis_service.move()
    await redis_service.move()
    await redis_service.move()
    print((await redis_service.get_snapshot()).model_dump_json())
    print(time.time())
    print(datetime.datetime.today())


asyncio.run(seeded_redis())