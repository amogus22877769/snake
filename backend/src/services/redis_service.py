from json import loads
from pathlib import Path
import asyncio

from redis.asyncio import Redis
from random import randint

from redis.commands.core import AsyncScript

from backend.src.pydantic_models.snapshot import Snapshot
from backend.src.types.direction import Direction
from backend.src.utils.inverse_direction import inverse_direction


class RedisService:
    def __init__(self) -> None:
        self.r: Redis = Redis(host="localhost", port=6379, decode_responses=True)
        self._load_scripts()

    def _load_scripts(self):
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

    async def change_direction(self, sid: str, new_direction: Direction) -> None:
        snake_name: str = await self.get_snake_scrit(args=[sid])
        if not snake_name:
            raise ValueError('You dont have a snake')
        current_direction: Direction = await self.r.get(
            f"snake:{snake_name}:direction"
        )
        if current_direction == inverse_direction(current_direction):
            raise ValueError("You cant go in the opposite direction")
        await self.r.set(f"snake:{snake_name}:direction", new_direction)

    async def get_snapshot(self) -> Snapshot:
        result: str = await self.get_snapshot_script()
        parsed_result: dict = loads(result)
        return Snapshot(**parsed_result)

    async def delete_snake(self, sid: str) -> None:
        if sid not in await self.get_sids_script():
            raise ValueError("There is no snake with such sid")
        await self.delete_snake_script(sid)

    async def run_loop(self):
        while True:
            await asyncio.gather(
                self.move_script(),
                asyncio.sleep(0.1),
            )

if __name__ == "__main__":

    async def main():
        redis_service = RedisService()
        # print(await redis_service.add_apple())
        # await redis_service.create_snake('maxim')
        # print(await redis_service.move())
        # print(await redis_service.get_snapshot())
        await redis_service.run_loop()

    asyncio.run(main())
