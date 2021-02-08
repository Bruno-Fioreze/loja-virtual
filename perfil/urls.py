from django.urls import path, include
from .views import Perfil, AtualizarPerfil, LoginPerfil, LogoutPerfil


urlpatterns = [
    path("", Perfil.as_view(), name="perfil"),
    path("atualizar-perfil/", AtualizarPerfil.as_view(), name="atualizar-perfil"),
    path("login/", LoginPerfil.as_view(), name="login-perfil"),
    path("logout/", LogoutPerfil.as_view(), name="login-perfil"),
]