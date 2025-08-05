import asyncio

import uvicorn

from backend.src.services.redis_service import RedisService
from backend.src.services.server_service import ServerService
from backend.src.services.socketio_service import socket_app

config = uvicorn.Config(socket_app, host="127.0.0.1", port=5000, log_level="info")
server = ServerService(config=config)

if __name__ == '__main__':
    with server.run_in_thread():
        asyncio.run(RedisService().run_move_loop())
