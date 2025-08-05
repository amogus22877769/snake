from pydantic import BaseModel, field_validator


class Block(BaseModel):
    left: int
    top: int

    @field_validator("left")
    def validate_left(cls, v):
        if v % 20 != 0:
            raise ValueError("Must be dividable by 20")
        return v

    @field_validator("top")
    def validate_top(cls, v):
        if v % 20 != 0:
            raise ValueError("Must be dividable by 20")
        return v
