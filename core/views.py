from django.contrib.auth.models import AnonymousUser
from django.http import HttpResponse
from django.views import View

from .socketio import sio


class SocketAuthView(View):
    @staticmethod
    def post(request):
        user = request.user
        sid = request.POST['sid']
        if isinstance(user, AnonymousUser):
            return HttpResponse('Войдите в систему для авторизации сокета')

        sio.users[sid] = user.username
        data = {
            'isAuthorized': True
        }
        sio.emit('isAuthorized', data)
        print(f'Authorized: {user.username} - {sid}')
        return HttpResponse('Сокет успешно авторизован')
