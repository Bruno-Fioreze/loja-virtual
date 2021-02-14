from django import forms
from .models import PerfilUser
from django.contrib.auth.models import User

class PerfilUserForm(forms.ModelForm):
    class Meta:
        model = PerfilUser
        fields = '__all__'
        exclude = ('user',)

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
        password_diferente = "As senhas não batem."
        password_tamanho = "Infome pelo menos 6 caracteres para a senha."

        if self.usuario:
            if user_authentica:
                if user_authentica.username != username:
                    mensagens_erro["username"] = usuario_existe

            if email_authentica:
                if email != email_authentica.email:
                    mensagens_erro["email"] = email_existe

            if password:
                if password != confirmacao_senha:
                    mensagens_erro["password"] = password_diferente
                    mensagens_erro["confirmacao_senha"] = password_diferente
                if len(password) < 6:
                    mensagens_erro["password"] = password_tamanho

        else:
            if user_authentica:
                mensagens_erro["username"] = usuario_existe

            if email_authentica.email:
                mensagens_erro["email"] = email_existe

            if password != confirmacao_senha:
                mensagens_erro["password"] = password_diferente
                mensagens_erro["confirmacao_senha"] = password_diferente

            if len(password) < 6:
                mensagens_erro["password"] = password_tamanho

        if mensagens_erro:
            raise (forms.ValidationError(mensagens_erro))