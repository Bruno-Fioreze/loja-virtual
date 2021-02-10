from django import forms
from .models import PerfilUser
from django.contrib.auth.models import User


class PerfilForm(forms.ModelForm):
    class Meta:
        model = PerfilUser
        fields = "__all__"
        exclude = ('user',)

class UserForm(forms.ModelForm):

    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(),
        label='Senha'
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)



    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "password", "email")

    def clean(self, *args, **kwargs):
        dados = self.data
        cleaned = self.cleaned_data
        print(dados)


