import re

SNAKE_NAME_REGEX = re.compile(r"^[a-z_]+$")


class SnakeName(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not isinstance(v, str):
            raise TypeError("String required")
        if not SNAKE_NAME_REGEX.fullmatch(v):
            raise ValueError(
                "Snake name can only contain lowercase letters and underscores"
            )
        return cls(v)
