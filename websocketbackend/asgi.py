"""
ASGI config for djangobnb project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter,URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator

from chat import routing
from chat.token_auth import TokenAuthMiddleware

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangobnb.settings')

application = ProtocolTypeRouter(
    {
        'http':get_asgi_application(),
        'websocket':TokenAuthMiddleware(
            URLRouter(routing.websocket_urlpatterns)
        )
        
    }
)