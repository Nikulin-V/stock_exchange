import socketio

from users.models import CustomUser

sio = socketio.Server(async_mode=None)
sio.users = dict()


@sio.event
def disconnect(sid):
    del sio.users[sid]
    print('Disconnected: ' + sid)


class SocketDisconnectedError(BaseException):
    pass


def get_socket_user(sid):
    try:
        return CustomUser.objects.get(username=sio.users[sid])
    except KeyError:
        sio.disconnect(sid)
        disconnect(sid)
        raise SocketDisconnectedError


# noinspection PyUnresolvedReferences
from .all_apis import *
