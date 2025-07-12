import pytest
import socketio

# Assuming your Socket.IO server is running on localhost:5000
SERVER_URL = "http://localhost:8000"


@pytest.fixture
def sio_client():
    client = socketio.Client()
    client.connect(SERVER_URL)
    yield client
    client.disconnect()


def test_connection(sio_client):
    assert sio_client.connected


# def test_emit_and_receive(sio_client):
#     received_data = {}
#
#     @sio_client.on('')
#     def on_response(data):
#         received_data['data'] = data
#
#     sio_client.emit('request_event', {'message': 'Hello'})
#     # Wait for the response event (adjust timeout as needed)
#     sio_client.sleep(1)
#
#     assert 'data' in received_data
#     assert received_data['data'] == 'Server received: Hello'
