# noinspection PyPackageRequirements
import socketio

from users.models import CustomUser

sio = socketio.Server(async_mode=None)
sio.users = dict()


@sio.event
def disconnect(sid):
    try:
        del sio.users[sid]
    except KeyError:
        pass
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
from core import all_apis
