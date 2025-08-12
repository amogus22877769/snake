from pydantic import BaseModel


class Config(BaseModel):
    CYCLE_FREQUENCY: int
    BOARD_TOP: int
    BOARD_LEFT: int
    BOARD_WIDTH: int
    BOARD_HEIGHT: int