import os

import eventlet.wsgi

# noinspection PyPackageRequirements
import socketio
from django.core.wsgi import get_wsgi_application

from core.socketio import sio

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stock_exchange.settings')

application = socketio.WSGIApp(sio, get_wsgi_application())
eventlet.wsgi.server(eventlet.listen(('', 8000)), application)
