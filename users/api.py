from core.socketio import sio
from users.models import CustomUser


@sio.on('getUser')
def getUser(sid, data):
    event_name = 'getUser'

    user = CustomUser.objects.filter(username=data['user']).all()[0]

    data = {
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'balance': user.balance,
    }

    sio.emit(event_name, data)
