import asyncio
from collections import namedtuple
from datetime import time
import json
from threading import Thread
from typing import Any
import socketio
from pydantic import ValidationError
from socketio import ASGIApp, AsyncServer
from fastapi import FastAPI

from backend.src.pydantic_models.block import Block
from backend.src.pydantic_models.new_client_snake import NewClientSnake
from backend.src.pydantic_models.new_direction import NewDirection
from backend.src.pydantic_models.new_snake import NewSnake
from backend.src.pydantic_models.snake import Snake
from backend.src.pydantic_models.snapshot import Snapshot
from backend.src.services.redis_service import RedisService
from backend.src.utils.get_millis import get_millis
from backend.src.utils.run_async_in_thread import run_async_in_thread

app = FastAPI()

sio: AsyncServer = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins="*")

socket_app: ASGIApp = socketio.ASGIApp(sio, other_asgi_app=app)

redis_service: RedisService = RedisService()

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

@app.on_event('startup')
async def startup():
    asyncio.create_task(redis_service.run_move_loop())

@sio.event
async def connect(sid, environ):
    async def handle_connect():
        print(f"Клиент подключился: {sid}")

    redis_service.event_queue.append(handle_connect())


@sio.event
async def disconnect(sid):
    async def handle_disconnect():
        print(f"Клиент отключился: {sid}")
        try:
            await redis_service.delete_snake(sid)
            if redis_service.get_number_of_snakes() == 0:
                pass

        except ValueError as e:
            print(str(e))

    redis_service.event_queue.append(handle_disconnect())


@sio.event
async def new_snake(sid, data: Any):
    async def handle_new_snake():
        try:
            new_sio_snake: NewSnake = NewSnake(**data)
            direction, top, left = await redis_service.create_snake(new_sio_snake.name, sid)
            snapshot: Snapshot = await redis_service.get_snapshot()
            print('Snapshot data: ', snapshot)
            await sio.emit('snapshot', snapshot.model_dump_json(), room=sid)
            print(f'Successfully sent snapshot to {sid}')
            print('Emitting new snake')
            await sio.emit('new_snake', NewClientSnake(
                name=new_sio_snake.name,
                blocks=[Block(top=top, left=left)],
                direction=direction,
                offset=snapshot.offset,
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

    redis_service.event_queue.append(handle_new_snake())

@sio.event
async def change_direction(sid, data: Any):
    async def handle_change_direction():
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

    await handle_change_direction()
