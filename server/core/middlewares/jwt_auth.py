from urllib.parse import parse_qs

from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

User = get_user_model()


class JWTAuthMiddleware:
    """
    Middleware de autenticação JWT para Django Channels.

    Responsabilidades:
    - Extrair token da query string
    - Validar JWT usando SimpleJWT
    - Popular scope["user"]
    """

    def __init__(self, inner):
        self.inner = inner
        self.jwt_auth = JWTAuthentication()

    async def __call__(self, scope, receive, send):
        scope["user"] = AnonymousUser()

        query_string = scope.get("query_string", b"").decode()
        params = parse_qs(query_string)

        token_list = params.get("token")

        if token_list:
            token = token_list[0]

            try:
                validated_token = self.jwt_auth.get_validated_token(token)
                user = self.jwt_auth.get_user(validated_token)
                scope["user"] = user
            except (InvalidToken, TokenError):
                pass

        return await self.inner(scope, receive, send)
