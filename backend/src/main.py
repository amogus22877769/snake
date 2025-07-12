import uvicorn
import socketio

sio = socketio.AsyncServer(async_mode="asgi")

socket_app = socketio.ASGIApp(sio)


@sio.event
async def connect(sid, environ):
    print(f"Клиент подключился: {sid}")
    await sio.emit("message", {"data": "Вы подключены"}, room=sid)


@sio.event
async def disconnect(sid):
    print(f"Клиент отключился: {sid}")


@sio.event
async def new_snake(sid, data):
    pass


if __name__ == "__main__":
    uvicorn.run(socket_app, host="0.0.0.0", port=8000)
