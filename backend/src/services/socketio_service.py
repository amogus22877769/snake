import asyncio
from datetime import time
import json
from typing import Any
import socketio
from pydantic import ValidationError
from socketio import ASGIApp, AsyncServer

from backend.src.pydantic_models.block import Block
from backend.src.pydantic_models.new_direction import NewDirection
from backend.src.pydantic_models.new_snake import NewSnake
from backend.src.pydantic_models.snake import Snake
from backend.src.pydantic_models.snapshot import Snapshot
from backend.src.services.redis_service import RedisService
from backend.src.utils.get_millis import get_millis

sio: AsyncServer = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins="*")

socket_app: ASGIApp = socketio.ASGIApp(sio)

redis_service: RedisService = RedisService()

ran: bool = False

async def run_apple_loop():
    print('Starting apple loop')
    while True:
        await asyncio.gather(
            add_apple(),
            asyncio.sleep(10)
        )

async def add_apple():
    _, top, left = await redis_service.add_apple()
    await sio.emit('new_apple', json.dumps({
        'top': top,
        'left': left,
    }))

@sio.event
async def connect(sid, environ):
    print(f"Клиент подключился: {sid}")

    global ran
    if not ran:
        ran = True
        await redis_service.run_move_loop()


@sio.event
async def disconnect(sid):
    print(f"Клиент отключился: {sid}")
    try:
        await redis_service.delete_snake(sid)
        if redis_service.get_number_of_snakes() == 0:
            pass

    except ValueError as e:
        print(str(e))


@sio.event
async def new_snake(sid, data: Any):
    try:
        new_sio_snake: NewSnake = NewSnake(**data)
        snapshot, direction, top, left = await redis_service.create_snake_and_get_snapshot(new_sio_snake.name, sid)
        print('Snapshot data: ', snapshot)
        await sio.emit('snapshot', snapshot.model_dump_json(), room=sid)
        print(f'Successfully sent snapshot to {sid}')
        print('Emitting new snake')
        await sio.emit('new_snake', Snake(
            name=new_sio_snake.name,
            blocks=[Block(top=top, left=left)],
            direction=direction,
        ).model_dump_json(), skip_sid=sid)
        # if redis_service.get_number_of_snakes() == 1:
        #     global should_apple_loop_run
        #     should_apple_loop_run = True
        #     await asyncio.gather(
        #         run_apple_loop(),
        #         redis_service.run_move_loop(),
        #     )
    except ValidationError as e:
        print(e.errors())
        await sio.emit("error", e.errors(), room=sid)
    except KeyError as e:
        print('KeyError: ', str(e))
        await sio.emit("error", str(e), room=sid)
    except ValueError as e:
        print('Value error: ', e)
        await sio.emit('error', str(e), room=sid)

@sio.event
async def change_direction(sid, data: Any):
    try:
        print(f'Recieved new direction for {sid}')
        new_validated_direction: NewDirection = NewDirection(**data)
        snake_name: str = await redis_service.change_direction(sid, new_validated_direction.direction)
        await sio.emit('change_direction', json.dumps({
            'name': snake_name,
            'direction': new_validated_direction.direction,
            'offset': new_validated_direction.offset,
        }), skip_sid=sid)
    except ValidationError as e:
        await sio.emit("error", e.errors(), room=sid)
    except (KeyError, ValueError) as e:
        await sio.emit("error", str(e), room=sid)
