from pydantic import BaseModel, validator


class Block(BaseModel):
    left: int
    top: int

    @validator("left")
    def validate_left(cls, v):
        if v % 20 != 0:
            raise ValueError("Must be dividable by 20")
        return v

    @validator("top")
    def validate_top(cls, v):
        if v % 20 != 0:
            raise ValueError("Must be dividable by 20")
        return v
