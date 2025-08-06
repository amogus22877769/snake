from pydantic import BaseModel

from backend.src.pydantic_models.apple import Apple
from backend.src.pydantic_models.snake import Snake


class Snapshot(BaseModel):
    cycle_offset: int
    creation_unix_time: float
    snakes: list[Snake]
    apples: list[Apple]
