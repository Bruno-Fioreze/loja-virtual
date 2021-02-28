from django.db import models
from django.contrib.auth.models import User
from django.forms import ValidationError
import re

class Pedido(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    total = models.FloatField()
    qtd_total = models.PositiveIntegerField() 
    status = models.CharField(
        default="C",
        max_length=50,
        choices=(
            ("A","Aprovado"),
            ("C","Criado"),
            ("R","Reprovado"),
            ("P","Pendente"),
            ("E","Enviado"),
            ("F","Finalizado"),
        )
    )


class ItemPedido(models.Model):
    id_produto = models.IntegerField(primary_key=True,blank=False,null=False)
    pedido = models.ForeignKey(Pedido,on_delete=models.CASCADE)
    produto = models.CharField(max_length=255)
    variacao = models.CharField(max_length=255)
    id_variacao = models.IntegerField()
    preco_promo = models.FloatField(default=0)
    quantidade = models.IntegerField()
    imagem = models.CharField(max_length=2000)

    def __str__(self):
        return f"Número pedido {self.pk}"

    class Meta:
        verbose_name = "Item do Pedido"
        verbose_name_plural = "Itens do Pedido"



