from django import forms
from .models import PerfilUser
from django.contrib.auth.models import User

class PerfilUserForm(forms.ModelForm):
    class Meta:
        model = PerfilUser
        fields = '__all__'
        exclude = ('usuario',)

class UserForm(forms.ModelForm):

    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(),
        label='Senha'
    )

    confirmacao_senha = forms.CharField(
        required=False,
        widget=forms.PasswordInput(),
        label='Confimação Senha'
    )

    def __init__(self, usuario=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.usuario = usuario

    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "password", "confirmacao_senha", "email",)

    def clean(self, *args, **kwargs):
        data = self.data
        cleaned = self.cleaned_data
        mensagens_erro = {}

        password = cleaned.get("password")
        email = cleaned.get("email")
        username = cleaned.get("username")
        confirmacao_senha = cleaned.get("confirmacao_senha")

        user_authentica = User.objects.get(username=username)
        email_authentica = User.objects.get(email=email)
        usuario_existe  = "Usuário já existe."
        email_existe = "E-mail já existe."
        password_diferente = "As senhas não são iguais."
        password_tamanho = "Infome pelo menos 6 caracteres para a senha."


        if self.usuario:
            if user_authentica.username != username:
                if user_authentica:
                    mensagens_erro["username"] = usuario_existe

            if password:
                if password != confirmacao_senha:
                    mensagens_erro["password"] = password_diferente
                    mensagens_erro["confirmacao_senha"] = password_diferente
                if len(password) < 6:
                    mensagens_erro["password"] = password_tamanho

            if email != email_authentica.email:
                if email_authentica:
                    mensagens_erro["email"] = email_existe

        else:
            mensagens_erro["username"] = "não logado"

        if mensagens_erro:
            raise (forms.ValidationError(mensagens_erro))