from django.db import models
import re
from django.contrib.auth.models import User
from django.forms import ValidationError


class PerfilUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    idade = models.IntegerField()
    data_nascimento = models.DateTimeField()
    cpf = models.CharField(max_length=11, blank=False, null=False)
    cep = models.CharField(max_length=8)
    endereco = models.CharField(max_length=255)
    complemento = models.CharField(max_length=50)
    bairro = models.CharField(max_length=150)
    cidade = models.CharField(max_length=255)
    estado = models.CharField(
        max_length=2,
        default="SP",
        choices=(
            ("AC","Acre"),
            ("SP","São Paulo")
        )
    )

    def clean(self):
        dict_erro = {}
        if re.search(r'[^0-9]',self.cep) or len(self.cep) < 8:
            dict_erro.update({"cep":"Cep Inválido"})

        raise ValidationError(dict_erro)


