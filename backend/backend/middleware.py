# coding=utf-8
from django.http import HttpRequest


class SetRemoteAddrMiddleware:
    """
    Middleware which passes the X-Real-IP header to REMOTE_ADDR if none
    has been set. This is mostly useful for local development in docker
    as everything goes through the nxing reverse proxy.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        remote_addr = request.META.get('REMOTE_ADDR')
        if remote_addr:
            # noinspection PyBroadException
            try:
                request.META['REMOTE_ADDR'] = request.META.get('HTTP_X_REAL_IP')
            except:
                pass

        response = self.get_response(request)

        return response
