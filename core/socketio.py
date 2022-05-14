import socketio

sio = socketio.Server(async_mode=None)
from users.api import getUser
from marketplace.api import getShares
