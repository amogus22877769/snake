import pytest

from backend.src.services.redis_service import RedisService


@pytest.fixture
def seeded_redis():
    redis_service: RedisService = RedisService()
    _, top, left = redis_service.create_snake('maxim', 'some_sid')
    redis_service.r.hset('apple:1', mapping={
        'left': left,
        'top': top + 20,
    })
    redis_service.move()
    assert not redis_service.r.exists('apple:1')

