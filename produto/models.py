from django.db import models
from PIL import Image
from django.conf import settings
from django.utils.text import slugify
import os



class Produto(models.Model):
    nome = models.CharField(max_length=255)
    descricao_curta = models.TextField(max_length=255)
    descricao_longa = models.TextField()
    img = models.ImageField(upload_to='produto/',blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True, null=True)
    preco_marketing = models.FloatField()
    preco_marketing_promo = models.FloatField(default=0,)
    tipo = models.CharField(
        default="v",
        max_length=1,
        choices=
        (
            ("V", "Variação"),
            ("S", "Simples")
        )
    )

    @staticmethod
    def redimenciona_img(img, novo_tamanho = 800):
        path_completo = os.path.join(settings.MEDIA_ROOT,img.name)
        img_pil = Image.open(path_completo)
        largura_original,altura_original = img_pil.size

        if largura_original <= novo_tamanho:
            img_pil.close()
            return

        novo_tamanho = round(novo_tamanho * altura_original / largura_original)
        imagem_reduzida = img_pil.resize((largura_original, altura_original), Image.LANCZOS)
        imagem_reduzida.save(
            path_completo,
            optimize=True,
            quality=50
        )

    def save(self,*args,**kwargs):
        if not self.slug:
            slug = f'{slugify(self.nome)}'
            self.slug = slug


        super().save(*args,**kwargs)
        if self.img:
            self.redimenciona_img(self.img, 800)

    def __str__(self):
        return self.nome


class Variacao(models.Model):
    produto = models.ForeignKey(Produto,on_delete=models.CASCADE)
    nome = models.CharField(max_length=50, blank=True, null=True)
    preco = models.FloatField()
    preco_promo = models.FloatField(default=0)
    estoque = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.nome or self.produto.nome

    class Meta:
        verbose_name = "Variação"
        verbose_name_plural = "Variações"