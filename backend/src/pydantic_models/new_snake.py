import re

from pydantic import BaseModel, field_validator


class NewSnake(BaseModel):
    name: str

    @field_validator('name')
    def validate_name(cls, v):
        if not re.compile(r"^[a-z_]+$").fullmatch(v):
            raise ValueError(
                "Snake name can only contain lowercase letters and underscores"
            )
        return v
