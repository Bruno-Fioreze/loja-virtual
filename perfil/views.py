from django.shortcuts import render
from django.views.generic.list import ListView
from django.views import View
from .forms import PerfilUser, UserForm
from .models import User, PerfilUser


class Perfil(View):
    template_name = "perfil/cadastre_se.html"

    def setup(self, request, *args, **kwargs):
        super().setup(self, request, *args, **kwargs)
        self.renderiza = render(request, self.template_name, {
            "user_form": UserForm(request.POST or None),
            "perfil_form": PerfilUser(request.POST or None),
        })

    def get(self, *args, **kwargs):
        return self.renderiza



class AtualizarPerfil(ListView):
    pass

class LoginPerfil(ListView):
    pass

class LogoutPerfil(ListView):
    pass