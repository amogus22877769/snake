from json import loads
from pathlib import Path
import asyncio
from typing import Callable, Coroutine

from redis.asyncio import Redis
from random import randint
from datetime import datetime

from redis.commands.core import AsyncScript

from backend.src.pydantic_models.snapshot import Snapshot
from backend.src.types.direction import Direction
from backend.src.utils.get_millis import get_millis
from backend.src.utils.get_millis_offset import get_millis_offset
from backend.src.utils.inverse_direction import inverse_direction

class RedisService:
    def __init__(self) -> None:
        self.r: Redis = Redis(host="localhost", port=6379, decode_responses=True)
        self._load_scripts()
        self.creation_cycle_offset: asyncio.Future | None = None
        self.cycle_offset: int | None = None

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
        random_left: int = randint(100, 1000)
        random_left -= random_left % 20
        random_top: int = randint(100, 1000)
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

    async def create_snake_and_get_snapshot(self, name: str, sid: str) -> tuple[Snapshot, Direction, int, int]:
        offset: int = await self.creation_cycle_offset
        try:
            direction, top, left = await self.create_snake(name, sid)
        except ValueError as e:
            raise e
        except TypeError as e:
            raise e
        result: str = await self.get_snapshot_script()
        parsed_result: dict = loads(result)
        return Snapshot(**parsed_result, offset=offset), direction, top, left

    async def delete_snake(self, sid: str) -> None:
        if sid not in await self.get_sids_script():
            raise ValueError("There is no snake with such sid")
        await self.delete_snake_script(sid)

    async def get_number_of_snakes(self) -> int:
        return len(await self.r.keys('snake:*:direction'))

    

    async def run_move_loop(self) -> None:
        if self.cycle_offset is None:
            cycle_offset = get_millis()
            print(f'{cycle_offset=}')
            self.creation_cycle_offset = asyncio.get_running_loop().create_future()
        else:
            raise BlockingIOError('Cant run 2 move loops simultaneously')
        iteration: int = 1
        while True:
            self.creation_cycle_offset.set_result(cycle_offset + (iteration - 1) * 100)
            self.creation_cycle_offset = asyncio.get_running_loop().create_future()
            estimated_end: int = cycle_offset + iteration * 100
            await asyncio.gather(
                self.move_script(),
                asyncio.sleep((estimated_end - get_millis()) / 1000),
            )
            real_end: int = get_millis()
            print(f'Real end: {real_end}, error: {real_end - estimated_end} or {abs(real_end - estimated_end)}%, keep it up!')
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
