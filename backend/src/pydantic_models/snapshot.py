from pydantic import BaseModel

class Snapshot(BaseModel):
    snakes: list[Snake]