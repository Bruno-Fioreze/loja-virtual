from django.shortcuts import render, get_object_or_404
from django.views.generic.list import ListView
from django.views import View
from .forms import PerfilUserForm, UserForm
from .models import PerfilUser
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
import copy



class Perfil(View):
    template_name = "perfil/cadastre_se.html"

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)
        self.perfil_user = None
        self.carrinho = copy.deepcopy(self.request.session.get("carrinho", {}))
        if self.request.user.is_authenticated:
            self.perfil_user = PerfilUser.objects.filter(user=self.request.user).first()

            self.dict_render = {
                'userForm': UserForm(
                    data=self.request.POST or None,
                    usuario=self.request.user,
                    instance=self.request.user
                ),
                'perfilUserForm': PerfilUserForm(
                    data=self.request.POST or None,
                    instance=self.perfil_user
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

        self.perfilUserForm = self.dict_render["perfilUserForm"]
        self.userForm = self.dict_render["userForm"]
        if self.request.user.is_authenticated:
            self.template_name = "perfil/atualizar.html"
        self.renderiza = render(self.request, self.template_name, self.dict_render)

    def get(self, *args, **kwargs):
        return self.renderiza

    def post(self, *args, **kwargs):

        if not self.perfilUserForm.is_valid() or not self.userForm.is_valid():
            return self.renderiza

        email = self.userForm.cleaned_data.get("email")
        username = self.userForm.cleaned_data.get("username")
        password = self.userForm.cleaned_data.get("password")

        if self.request.user.is_authenticated:
            user = get_object_or_404(
                User, username=self.request.user.username)
            if password:
                user.set_password(password)
            user.username = username
            user.email = email
            user.first_name = self.userForm.cleaned_data.get("first_name")
            user.last_name = self.userForm.cleaned_data.get("last_name")
            user.save()

            perfil_user = self.perfilUserForm.save(commit=False)
            perfil_user.user = self.request.user
            perfil_user.save()
        else:
            user = self.userForm.save(commit=False)
            user.set_password(password)
            user.save()

            perfil_user = self.perfilUserForm.save(commit=False)
            perfil_user.user = user
            perfil_user.save()

        if password:
            auth = authenticate(
                self.request,
                username=username,
                password=password
            )
            if auth:
                login(self.request, user=user)
        self.request.session["carrinho"] = self.carrinho
        self.request.session.save()
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


def get_hash(valor):
    print(valor)
    hasher = "pbkdf2_sha256"
    salt = "150000"
    return make_password(valor, salt=salt, hasher=hasher)
