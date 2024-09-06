# estoque/models.py
from django.db import models

class Segmento(models.Model):
    nome = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nome

class Produto(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)
    imagem = models.ImageField(upload_to='produtos/', blank=True, null=True)
    quantidade = models.IntegerField(default=0)
    preco_caixa = models.DecimalField(max_digits=10, decimal_places=2)
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    codigo_barras = models.CharField(max_length=50, blank=True, null=True)
    segmento = models.ForeignKey(Segmento, on_delete=models.CASCADE)
    data_ultima_entrada = models.DateField(auto_now_add=True)
    data_vencimento = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.nome

class EntradaProduto(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, related_name='entradas')
    quantidade = models.IntegerField()
    data_entrada = models.DateField(auto_now_add=True)
    data_vencimento = models.DateField()
    preco_compra = models.DecimalField(max_digits=10, decimal_places=2)
    codigo_entrada = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f"{self.produto.nome} - {self.codigo_entrada}"

# Modelo para registrar as saídas de estoque
class SaidaProduto(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, related_name='saidas')
    entrada = models.ForeignKey(EntradaProduto, on_delete=models.CASCADE)  # Relaciona com a entrada específica
    quantidade = models.IntegerField()
    data_saida = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.produto.nome} - {self.quantidade} saído(s) em {self.data_saida}"
