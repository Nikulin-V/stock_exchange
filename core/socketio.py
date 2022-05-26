# noinspection PyPackageRequirements
import socketio

from users.models import CustomUser

sio = socketio.Server(async_mode=None)
sio.users = dict()


@sio.event
def disconnect(sid):
    """
    Event of socket disconnection

    :param sid: user socket session id
    """
    try:
        del sio.users[sid]
    except KeyError:
        pass


class SocketDisconnectedError(BaseException):
    pass


def get_socket_user(sid) -> CustomUser:
    """
    Get user object by its socket session id

    :param sid: user socket session id
    :return: user object
    """
    try:
        return CustomUser.objects.get(username=sio.users[sid])
    except KeyError:
        sio.disconnect(sid)
        disconnect(sid)
        raise SocketDisconnectedError


# noinspection PyUnresolvedReferences
from core import all_apis
