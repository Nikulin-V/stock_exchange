import os
import sys

import eventlet.wsgi

# noinspection PyPackageRequirements
import socketio
from django.core.wsgi import get_wsgi_application

from core.socketio import sio


if sys.version_info.major < 3 or sys.version_info.minor < 9:
    print("Python version 3.9 required.")
    exit(1)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stock_exchange.settings')

application = socketio.WSGIApp(sio, get_wsgi_application())
eventlet.wsgi.server(eventlet.listen(('', 8000)), application)
