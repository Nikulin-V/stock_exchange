from core.socketio import sio, get_socket_user


@sio.on('getUser')
def getUser(sid, data):
    event_name = 'getUser'

    user = get_socket_user(sid)

    data = {
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'balance': user.balance,
    }

    sio.emit(event_name, data)
