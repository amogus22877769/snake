from pydantic import BaseModel, Field

class Snake(BaseModel):
    name: str = Field(pattern='[a-zA-Z]')

if __name__ == '__main__':
    Snake(name='maxim123')