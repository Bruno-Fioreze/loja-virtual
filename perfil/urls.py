from django.urls import path, include
from .views import Perfil, AtualizarPerfil, CadastrarPerfil


urlpatterns = [
    path("", Perfil.as_view(), name="perfil"),
    path("cadastrar/", CadastrarPerfil.as_view(), name="cadastrar-perfil"),
    path("atualizar-perfil/", AtualizarPerfil.as_view(), name="atualizar-perfil"),
]