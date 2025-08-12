from collections import deque
from json import loads
from pathlib import Path
import asyncio
from typing import Callable, Coroutine, Awaitable

from redis.asyncio import Redis
from random import randint
from datetime import datetime

from redis.commands.core import AsyncScript

from backend.src.config import config
from backend.src.pydantic_models.snapshot import Snapshot
from backend.src.types.direction import Direction
from backend.src.utils.get_millis import get_millis
from backend.src.utils.get_millis_offset import get_millis_offset
from backend.src.utils.inverse_direction import inverse_direction
from backend.src.utils.sleep import sleep


class RedisService:
    def __init__(self) -> None:
        self.r: Redis = Redis(host="localhost", port=6379, decode_responses=True)
        self._load_scripts()
        self.cycle_offset: int | None = None
        self.event_queue: deque[Awaitable[None]] = deque()

    def _load_scripts(self) -> None:
        script_dir: Path = Path(__file__).parent.parent / "redis_scripts"
        self.create_snake_script: AsyncScript = self._register_script(
            script_dir / "create_snake.lua"
        )
        self.move_script: AsyncScript = self._register_script(script_dir / "move.lua")
        self.add_apple_script: AsyncScript = self._register_script(
            script_dir / "add_apple.lua"
        )
        self.change_direction_script: AsyncScript = self._register_script(
            script_dir / "change_direction.lua"
        )
        self.get_snapshot_script: AsyncScript = self._register_script(
            script_dir / "get_snapshot.lua"
        )
        self.delete_snake_script: AsyncScript = self._register_script(
            script_dir / "delete_snake.lua"
        )
        self.get_sids_script: AsyncScript = self._register_script(
            script_dir / "get_sids.lua"
        )
        self.get_snake_scrit: AsyncScript = self._register_script(
            script_dir / 'get_snake.lua'
        )

    def _register_script(self, script_path: Path) -> AsyncScript:
        with open(script_path, "r") as f:
            script_content: str = f.read()
        return self.r.register_script(script_content)

    async def create_snake(self, name: str, sid: str) -> tuple[Direction, int, int]:
        if sid in await self.get_sids_script():
            raise ValueError("You already have a snake")
        if await self.r.exists(f"snake:{name}:direction"):
            raise KeyError("Snake with such name already exists. Try another name")
        random_left: int = randint(100, 700)
        random_left -= random_left % 20
        random_top: int = randint(100, 700)
        random_top -= random_top % 20
        await self.create_snake_script(
            keys=[name], args=["up", random_left, random_top, sid]
        )
        return "up", random_top, random_left

    async def move(self) -> None:
        print("Moving")
        await self.move_script()

    async def add_apple(self) -> tuple[int, int, int]:
        random_left: int = randint(100, 1000)
        random_left -= random_left % 20
        random_top: int = randint(100, 1000)
        random_top -= random_top % 20
        index: int = await self.add_apple_script(args=[random_left, random_top])
        return index, random_top, random_left

    async def change_direction(self, sid: str, new_direction: Direction) -> str:
        snake_name: str = await self.get_snake_scrit(args=[sid])
        if not snake_name:
            raise ValueError('You dont have a snake')
        current_direction: Direction = await self.r.get(
            f"snake:{snake_name}:direction"
        )
        if current_direction == inverse_direction(current_direction):
            raise ValueError("You cant go in the opposite direction")
        await self.r.set(f"snake:{snake_name}:direction", new_direction)
        return snake_name

    async def get_snapshot(self) -> Snapshot:
        result: str = await self.get_snapshot_script()
        parsed_result: dict = loads(result)
        return Snapshot(**parsed_result, offset=self.cycle_offset)

    async def delete_snake(self, sid: str) -> None:
        if sid not in await self.get_sids_script():
            raise ValueError("There is no snake with such sid")
        await self.delete_snake_script(sid)

    async def get_number_of_snakes(self) -> int:
        return len(await self.r.keys('snake:*:direction'))

    async def run_move_loop(self) -> None:
        if self.cycle_offset is None:
            offset: int = get_millis()
            cycle_offset = offset
            print(f'{cycle_offset=}')
        else:
            raise BlockingIOError('Cant run 2 move loops simultaneously')
        iteration: int = 1
        while True:
            await self.move_script()
            self.cycle_offset = offset + (iteration - 1) * config.CYCLE_FREQUENCY
            while self.event_queue:
                await self.event_queue.popleft()
            estimated_end: int = self.cycle_offset + config.CYCLE_FREQUENCY
            await sleep(
                max((estimated_end - get_millis()) / 1000, 0)
            )
            real_end: int = get_millis()
            print(
                f'Real end: {real_end}, error: {real_end - estimated_end} or {abs(real_end - estimated_end)}%, keep it up!')
            iteration += 1


if __name__ == "__main__":
    async def main():
        redis_service = RedisService()
        # print(await redis_service.add_apple())
        # await redis_service.create_snake('maxim')
        # print(await redis_service.move())
        # print(await redis_service.get_snapshot())
        await redis_service.run_move_loop()


    asyncio.run(main())
