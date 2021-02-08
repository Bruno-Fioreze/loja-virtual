# Generated by Django 3.1.6 on 2021-02-03 21:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Produto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=255)),
                ('descricao_curta', models.TextField(max_length=255)),
                ('descricao_longa', models.TextField()),
                ('descricao_img', models.ImageField(blank=True, null=True, upload_to='produto/')),
                ('descricao_slug', models.SlugField(unique=True)),
                ('preco_marketing', models.FloatField()),
                ('preco_marketing_promo', models.FloatField(default=0)),
                ('tipo', models.CharField(choices=[('V', 'Variação'), ('S', 'Simples')], default='v', max_length=1)),
            ],
        ),
    ]