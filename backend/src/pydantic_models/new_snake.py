from pydantic import BaseModel

from backend.src.types.snake_name import SnakeName


class NewSnake(BaseModel):
    name: SnakeName
