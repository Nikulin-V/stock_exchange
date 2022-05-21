from __future__ import absolute_import, division, print_function

from threading import local

from django.utils.deprecation import MiddlewareMixin

_thread_locals = local()


def get_current_request():
    return getattr(_thread_locals, 'request', None)


def get_current_user():
    request = get_current_request()
    if request:
        return getattr(request, 'user', None)


class ThreadLocalMiddleware(MiddlewareMixin):
    @staticmethod
    def process_request(request):
        _thread_locals.request = request

    @staticmethod
    def process_response(*args):
        request, response = args
        if hasattr(_thread_locals, 'request'):
            del _thread_locals.request
        return response
