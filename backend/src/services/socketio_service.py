import asyncio
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
        direction, top, left = await redis_service.create_snake(new_sio_snake.name, sid)
        snapshot: Snapshot = await redis_service.get_snapshot()
        print('Snapshot data: ', snapshot)
        await sio.emit('snapshot', snapshot.model_dump_json(), room=sid)
        print(f'Successfully sent snapshot to {sid}')
        print('Emitting new snake')
        await sio.emit('new_snake', Snake(
            name=new_sio_snake.name,
            blocks=[Block(top=top, left=left)],
            direction=direction,
        ).model_dump_json(), skip_sid=sid)
        global ran
        if not ran:
            ran = True
            await run_apple_loop()
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

@sio.event
async def change_direction(sid, new_direction: Any):
    try:
        print(f'Recieved new direction for {sid}: {new_direction}')
        new_validated_direction: NewDirection = NewDirection(direction=new_direction)
        snake_name: str = await redis_service.change_direction(sid, new_validated_direction.direction)
        await sio.emit('change_direction', json.dumps({
            'name': snake_name,
            'direction': new_direction,
        }), skip_sid=sid)
    except ValidationError as e:
        await sio.emit("error", e.errors(), room=sid)
    except (KeyError, ValueError) as e:
        await sio.emit("error", str(e), room=sid)
