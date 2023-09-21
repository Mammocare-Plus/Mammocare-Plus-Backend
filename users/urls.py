from django.urls import path
from rest_framework.routers import SimpleRouter
from rest_framework.views import APIView
from rest_framework.response import Response
from users.views import (
    MCPUserLoginView,
    MCPUserRegisterView,
    MCPUserLogoutView,
    MCPUserViewSet,
)
from rest_framework_simplejwt.views import (
    TokenRefreshView
)

router = SimpleRouter()
router.register(r'users', MCPUserViewSet, basename='users')

class HomeView(APIView):
    def get(self, request):
        return Response({
            'message': 'Welcome to MCP users API',
            'endpoints': [
                '/login/',
                '/register/',
                '/logout/',
                '/users/',
            ]
        })

urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path('register/', MCPUserRegisterView.as_view(),name="register"),
    path('login/', MCPUserLoginView.as_view(),name="login"),
    path('logout/', MCPUserLogoutView.as_view(), name="logout"),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
] + router.urls