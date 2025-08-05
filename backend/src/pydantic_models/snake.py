from backend.src.pydantic_models.block import Block
from backend.src.pydantic_models.new_snake import NewSnake
from backend.src.types.direction import Direction


class Snake(NewSnake):
    blocks: list[Block]
    direction: Direction
