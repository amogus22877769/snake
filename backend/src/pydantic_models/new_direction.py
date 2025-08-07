from pydantic import BaseModel, field_validator

from backend.src.types.direction import Direction
from backend.src.utils.get_millis import get_millis


class NewDirection(BaseModel):
    direction: Direction
    offset: int

    @field_validator('offset')
    def validate_offset(cls, v):
        print('Received new direction, latency is ', get_millis() - v)
        if get_millis() - v > 100:
            raise Exception('Time diff must be less than 100ms')
        return v
