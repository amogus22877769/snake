from pathlib import Path
import asyncio

from redis.asyncio import Redis
from random import randint

class RedisService:
    def __init__(self) -> None:
        self.r = Redis(host='localhost', port=6379, decode_responses=True)
        self._load_scripts()

    def _load_scripts(self):
        script_dir = Path(__file__).parent.parent / 'redis_scripts'
        self.create_snake_script = self._register_script(script_dir / 'create_snake.lua')
        self.move_script = self._register_script(script_dir / 'move.lua')
        self.add_apple_script = self._register_script(script_dir / 'add_apple.lua')

    def _register_script(self, script_path: Path):
        with open(script_path, 'r') as f:
            script_content: str = f.read()
        return self.r.register_script(script_content)

    async def create_snake(self, name: str) -> tuple[str, int, int]:
        if await self.r.exists(f'snake:{name}:direction'):
            raise KeyError('Snake with such name already exists. Try another name')
        random_left: int = randint(100, 1000)
        random_left -= random_left % 20
        random_top: int = randint(100, 1000)
        random_top -= random_top % 20
        await self.create_snake_script(
            keys=[name],
            args=['up', random_left, random_top]
        )
        return 'up', random_top, random_left

    async def move(self) -> None:
        print('Moving')
        await self.move_script()

    async def add_apple(self) -> tuple[int, int, int]:
        random_left: int = randint(100, 1000)
        random_left -= random_left % 20
        random_top: int = randint(100, 1000)
        random_top -= random_top % 20
        index: int = await self.add_apple_script(
            args=[random_left, random_top]
        )
        return index, random_top, random_left


if __name__ == '__main__':
    async def main():
        redis_service = RedisService()
        print(await redis_service.add_apple())
        # await redis_service.create_snake('maxim')
        # await redis_service.move()
    asyncio.run(main())
