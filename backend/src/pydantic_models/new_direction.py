from pydantic import BaseModel

from backend.src.types.direction import Direction


class NewDirection(BaseModel):
    direction: Direction
