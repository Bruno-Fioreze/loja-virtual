from django.urls import path, include
from .views import Perfil


urlpatterns = [
    path("", Perfil.as_view(), name="perfil"),
]