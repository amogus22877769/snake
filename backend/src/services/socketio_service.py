import asyncio
from typing import Any
from threading import Thread
import uvicorn
import socketio
from pydantic import ValidationError

from backend.src.pydantic_models.new_direction import NewDirection
from backend.src.pydantic_models.new_snake import NewSnake
from backend.src.services.redis_service import RedisService

sio = socketio.AsyncServer(async_mode="asgi")

socket_app = socketio.ASGIApp(sio)

redis_service = RedisService()


@sio.event
async def connect(sid):
    print(f"Клиент подключился: {sid}")
    await sio.emit("message", {"data": "Вы подключены"}, room=sid)


@sio.event
async def disconnect(sid):
    print(f"Клиент отключился: {sid}")
    try:
        await redis_service.delete_snake(sid)
    except ValueError as e:
        print(e)


@sio.event
async def new_snake(sid, data: Any):
    try:
        new_sio_snake: NewSnake = NewSnake(**data)
        await redis_service.create_snake(new_sio_snake.name, sid)
    except ValidationError as e:
        await sio.emit("error", e.errors(), room=sid)
    except KeyError as e:
        await sio.emit("error", e, room=sid)

@sio.event
async def change_direction(sid, new_direction: Any):
    try:
        new_validated_direction: NewDirection = NewDirection(direction=new_direction)
        await redis_service.change_direction(sid, new_validated_direction.direction)
    except ValidationError as e:
        await sio.emit("error", e.errors(), room=sid)
    except (KeyError, ValueError) as e:
        await sio.emit("error", e, room=sid)

def between_callback():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    loop.run_until_complete(redis_service.run_loop())
    loop.close()

if __name__ == "__main__":
    Thread(target=between_callback).run()
    print(1)
    Thread(target=uvicorn.run, args=[socket_app], kwargs={
        'host': '0.0.0.0',
        'port': 8000,
    }).run()
    print(1)
