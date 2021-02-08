from django import forms
from .models import PerfilUser
from django.contrib.auth.models import User


class PerfilForm(forms.ModelForm):
    class Meta:
        model = PerfilUser
        fields = "__all__"
        exclude = ('user',)

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "password", "email")

    def clean(self, *args, **kwargs):
        dados = self.data
        cleaned = self.cleaned_data

