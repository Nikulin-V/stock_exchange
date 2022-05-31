from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import AnonymousUser
from django.http import HttpResponse
from django.views import View

from .socketio import sio


class SocketAuthView(LoginRequiredMixin, View):
    """Page of connecting socket session id and user"""
    event_name = 'isAuthorized'

    def post(self, request):
        user = request.user
        sid = request.POST['sid']
        if isinstance(user, AnonymousUser):
            return HttpResponse('Войдите в систему для авторизации сокета')

        sio.users[sid] = user.username
        data = {self.event_name: True}
        sio.emit(self.event_name, data, to=sid)
        return HttpResponse('Сокет успешно авторизован')
