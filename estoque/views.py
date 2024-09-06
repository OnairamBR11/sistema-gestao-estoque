# estoque/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Produto, Segmento, EntradaProduto, SaidaProduto
from .forms import ProdutoForm, SegmentoForm, EntradaProdutoForm, SaidaProdutoForm
from django.db.models import Q

def listar_produtos(request):
    query = request.GET.get('q')  # Captura o termo de pesquisa da URL
    produtos = Produto.objects.all()

    if query:
        # Filtra produtos pelo nome ou segmento usando Q objects
        produtos = produtos.filter(
            Q(nome__icontains=query) |
            Q(segmento__nome__icontains=query)
        )
    
    return render(request, 'estoque/listar_produtos.html', {'produtos': produtos, 'query': query})

def saida_estoque(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    if request.method == 'POST':
        form = SaidaProdutoForm(request.POST, produto=produto)
        if form.is_valid():
            entrada = form.cleaned_data['entrada']
            quantidade = form.cleaned_data['quantidade']

            # Verifica se a quantidade solicitada está disponível na entrada
            if entrada.quantidade < quantidade:
                form.add_error('quantidade', 'A quantidade excede a disponível na entrada selecionada.')
            else:
                # Registra a saída de estoque
                saida = SaidaProduto(produto=produto, entrada=entrada, quantidade=quantidade)
                saida.save()

                # Atualiza a quantidade da entrada e do produto
                entrada.quantidade -= quantidade
                entrada.save()
                produto.quantidade -= quantidade
                produto.save()
                
                return JsonResponse({'success': True})  # Retorno AJAX para sucesso
        return JsonResponse({'success': False, 'error': form.errors})  # Retorno AJAX para erros
    else:
        form = SaidaProdutoForm(produto=produto)
    return render(request, 'estoque/saida_estoque.html', {'form': form, 'produto': produto})

def adicionar_entrada(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    if request.method == 'POST':
        form = EntradaProdutoForm(request.POST)
        if form.is_valid():
            entrada = form.save(commit=False)
            entrada.produto = produto
            entrada.save()
            # Atualiza a quantidade do produto com a nova entrada
            produto.quantidade += entrada.quantidade
            produto.data_vencimento = entrada.data_vencimento  # Atualiza a data de validade para o mais recente
            produto.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': form.errors})
    else:
        form = EntradaProdutoForm(initial={'produto': produto})
    return render(request, 'estoque/adicionar_entrada.html', {'form': form, 'produto': produto})

def criar_segmento(request):
    if request.method == 'POST':
        form = SegmentoForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': form.errors})
    else:
        form = SegmentoForm()
    return render(request, 'estoque/criar_segmento.html', {'form': form})

def criar_produto(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': form.errors})
    else:
        form = ProdutoForm()
    return render(request, 'estoque/criar_produto.html', {'form': form})

def detalhar_produto(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    entradas = produto.entradas.all()  # Recupera todas as entradas associadas ao produto
    saidas = produto.saidas.all()      # Recupera todas as saídas associadas ao produto
    return render(request, 'estoque/detalhar_produto.html', {'produto': produto, 'entradas': entradas, 'saidas': saidas})

def editar_produto(request, pk):
    produto = get_object_or_404(Produto, pk=pk)  # Busca o produto pelo ID
    if request.method == 'POST':
        form = ProdutoForm(request.POST, request.FILES, instance=produto)  # Instancia o formulário com o produto existente
        if form.is_valid():
            form.save()  # Salva o produto com os novos dados
            return JsonResponse({'success': True})  # Retorna um JSON de sucesso (ou redireciona conforme necessário)
        else:
            return JsonResponse({'success': False, 'error': form.errors})  # Retorna erros de validação, se houver
    else:
        form = ProdutoForm(instance=produto)  # Renderiza o formulário com os dados do produto atual
    return render(request, 'estoque/editar_produto.html', {'form': form, 'produto': produto})

def deletar_produto(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    if request.method == 'POST':
        produto.delete()
        # Retorna uma resposta JSON se for uma requisição AJAX
        if request.is_ajax():
            return JsonResponse({'success': True})
        # Redireciona para a listagem de produtos após a exclusão
        return redirect('listar_produtos')
    return render(request, 'estoque/detalhar_produto.html', {'produto': produto})
