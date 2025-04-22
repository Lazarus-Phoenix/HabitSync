from django.urls import include, path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.contrib import admin


"""
Вы сможете увидеть документацию API, перейдя по URL-адресу 
http://localhost:8000/swagger/
 для Swagger UI или 
http://localhost:8000/redoc/
 для Redoc.
"""

schema_view = get_schema_view(
    openapi.Info(
        title="API Documentation app HabitSync",
        default_version='v1',
        description="API трекер привычек с синхронизацией в телеграм",
        terms_of_service="https://www.example.com/policies/terms/",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path(r"admin/", admin.site.urls),
    path(r"habits/", include("habits.urls", namespace="habits")),
    path(r"users/", include("users.urls", namespace="users")),
    path(
        'swagger/', schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui'
    ),
    path(
        'redoc/', schema_view.with_ui('redoc', cache_timeout=0),
        name='schema-redoc'
    ),
]