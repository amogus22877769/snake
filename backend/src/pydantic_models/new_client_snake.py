from backend.src.pydantic_models.snake import Snake


class NewClientSnake(Snake):
    offset: int
