from django.http import HttpResponse
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.permissions import AllowAny
from .serializers import RegisterSerializer
from django.utils import timezone


class RegisterView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request: Request) -> Response:
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "User registered successfully"}, status=201)

        return Response(getattr(serializer, "errors"), status=400)


class LoginView(APIView):
    def post(self, request: Request) -> Response:
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)
        if user is not None:
            # Atualiza last_login manualmente
            user.last_login = timezone.now()
            user.save(update_fields=["last_login"])

            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token)
            })
        else:
            return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


def websocket_test_view(request):
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Teste WebSocket</title>
    </head>
    <body>
        <h1>Teste WebSocket</h1>
        <button onclick="sendMessage()">Enviar mensagem</button>

        <script>
            const socket = new WebSocket("ws://localhost:8000/ws/game/");

            socket.onopen = () => {
                console.log("Conectado ao WebSocket");
            };

            socket.onmessage = (event) => {
                console.log("Mensagem recebida:", event.data);
            };

            socket.onclose = () => {
                console.log("WebSocket fechado");
            };

            function sendMessage() {
                socket.send("Olá do navegador!");
            }
        </script>
    </body>
    </html>
    """
    return HttpResponse(html)
