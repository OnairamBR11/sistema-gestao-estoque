# Generated by Django 5.1.1 on 2024-09-06 13:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Produto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('descricao', models.TextField(blank=True, null=True)),
                ('imagem', models.ImageField(blank=True, null=True, upload_to='produtos/')),
                ('quantidade', models.IntegerField(default=0)),
                ('preco_caixa', models.DecimalField(decimal_places=2, max_digits=10)),
                ('preco_unitario', models.DecimalField(decimal_places=2, max_digits=10)),
                ('codigo_barras', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Segmento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='EntradaProduto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantidade', models.IntegerField()),
                ('data_entrada', models.DateField(auto_now_add=True)),
                ('data_vencimento', models.DateField()),
                ('preco_compra', models.DecimalField(decimal_places=2, max_digits=10)),
                ('codigo_entrada', models.CharField(max_length=50, unique=True)),
                ('produto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='entradas', to='estoque.produto')),
            ],
        ),
        migrations.AddField(
            model_name='produto',
            name='segmento',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='estoque.segmento'),
        ),
    ]
