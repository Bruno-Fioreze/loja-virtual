from django.shortcuts import render
from django.views.generic.list import ListView
from django.views import View
from .forms import PerfilUserForm, UserForm
from .models import User, PerfilUser
from django.views.decorators.http import require_http_methods



class Perfil(View):
    template_name = "perfil/cadastre_se.html"
    def setup(self, *args, **kwargs):
        super().setup(*args,**kwargs)
        if self.request.user.is_authenticated:
            self.dict_render = {
                'userForm': UserForm(
                    data=self.request.POST or None,
                    usuario=self.request.user,
                    instance=self.request.user
                ),
                'perfilUserForm': PerfilUserForm(
                    data=self.request.POST or None,
                )
            }
        else:
            self.dict_render = {
                'userForm': UserForm(
                    data=self.request.POST or None,
                ),
                'perfilUserForm': PerfilUserForm(
                    data=self.request.POST or None
                )
            }

        self.renderiza = render(self.request, self.template_name, self.dict_render)

    def get(self, *args, **kwargs):
        return self.renderiza

    def post(self, *args, **kwargs):
        return self.renderiza


class CadastrarPerfil(View):
    def post(self, *args, **kwargs):
        print(self.request.POST)


class AtualizarPerfil(ListView):
    pass

class LoginPerfil(ListView):
    pass

class LogoutPerfil(ListView):
    pass