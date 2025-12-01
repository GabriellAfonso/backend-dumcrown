from django.urls import path
from .views import RegisterView, LoginView, websocket_test_view
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('game/', websocket_test_view, name='game'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
