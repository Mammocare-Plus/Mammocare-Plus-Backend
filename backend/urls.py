from django.contrib import admin
from django.urls import path, include
from rest_framework.views import APIView
from rest_framework.response import Response

class HomeView(APIView):
    def get(self, request):
        return Response({
            'message': 'Welcome to MCP Backend',
            'endpoints': [
                '/users/',
                '/api/',
            ]
        })

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("admin/", admin.site.urls),
    path("users/", include("users.urls")),
    path("api/", include("api.urls")),
]
