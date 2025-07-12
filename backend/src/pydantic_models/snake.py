from pydantic import BaseModel

from backend.src.pydantic_models.block import Block
from backend.src.types.direction import Direction
from backend.src.types.snake_name import SnakeName


class Snake(BaseModel):
    name: SnakeName
    blocks: list[Block]
    direction: Direction
