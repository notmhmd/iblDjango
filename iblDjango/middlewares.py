from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from django.contrib.auth.models import User, AnonymousUser
from rest_framework.authtoken.models import Token


@database_sync_to_async
def get_user_from_token(token):
    token = Token.objects.get(key=token)
    return token.user


class QueryParamsTokenAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        token_key = scope['query_string'].decode().split('=')[1]
        try:
            user = await get_user_from_token(token_key)
            scope['user'] = user
        except Token.DoesNotExist:
            scope['user'] = AnonymousUser()
        return await super().__call__(scope, receive, send)
