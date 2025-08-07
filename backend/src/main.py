import uvicorn

if __name__ == '__main__':
    uvicorn.run('services.socketio_service:socket_app', port=5000)
