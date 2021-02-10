from django.shortcuts import render
from django.views.generic.list import ListView
from django.views import View
from .forms import PerfilUser, UserForm
from .models import User, PerfilUser


class Perfil(View):
    template_name = "perfil/cadastre_se.html"

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)
        if self.request.user.is_authenticated:

            dict_render = {
                "user_form": UserForm(
                    self.request.POST or None,

                    instance=self.request.user,
                ),
                "perfil_form": PerfilUser(self.request.POST or None),
            }
            self.renderiza = render(self.request, self.template_name, dict_render)
        else:
            dict_render = {
                "user_form": UserForm(self.request.POST or None),
                "perfil_form": PerfilUser(self.request.POST or None),
            }
            self.renderiza = render(self.request, self.template_name, dict_render)
    def get(self, *args, **kwargs):
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