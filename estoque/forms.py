# estoque/forms.py
from django import forms
from .models import Produto, Segmento, EntradaProduto

class SegmentoForm(forms.ModelForm):
    class Meta:
        model = Segmento
        fields = ['nome']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do Segmento'}),
        }

class SaidaProdutoForm(forms.Form):
    entrada = forms.ModelChoiceField(
        queryset=EntradaProduto.objects.none(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Selecionar Entrada'
    )
    quantidade = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Quantidade'}),
        label='Quantidade a Retirar'
    )

    def __init__(self, *args, **kwargs):
        produto = kwargs.pop('produto')
        super().__init__(*args, **kwargs)
        self.fields['entrada'].queryset = EntradaProduto.objects.filter(produto=produto).order_by('data_vencimento')

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'descricao', 'imagem', 'quantidade', 'preco_caixa', 'preco_unitario', 'codigo_barras', 'segmento', 'data_vencimento']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do Produto'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descrição'}),
            'imagem': forms.FileInput(attrs={'class': 'form-control'}),
            'quantidade': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Quantidade'}),
            'preco_caixa': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Preço da Caixa'}),
            'preco_unitario': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Preço Unitário'}),
            'codigo_barras': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Código de Barras'}),
            'segmento': forms.Select(attrs={'class': 'form-control'}),
            'data_vencimento': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Data de Vencimento', 'type': 'date'}),
        }

class EntradaProdutoForm(forms.ModelForm):
    class Meta:
        model = EntradaProduto
        fields = ['produto', 'quantidade', 'data_vencimento', 'preco_compra', 'codigo_entrada']
        widgets = {
            'produto': forms.Select(attrs={'class': 'form-control'}),
            'quantidade': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Quantidade'}),
            'data_vencimento': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Data de Vencimento', 'type': 'date'}),
            'preco_compra': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Preço de Compra'}),
            'codigo_entrada': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Código da Entrada'}),
        }
