"""
ASGI config for iblDjango project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""
import os

from django.conf import settings
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from iblDjango.urls import websocket_urlpatterns
from iblDjango.middlewares import QueryParamsTokenAuthMiddleware

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'iblDjango.settings')


application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": QueryParamsTokenAuthMiddleware(
        AuthMiddlewareStack(
            URLRouter(
                websocket_urlpatterns
            )
        )
    ),
})