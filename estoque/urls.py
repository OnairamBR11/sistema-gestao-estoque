# estoque/urls.py
from django.urls import path
from .views import listar_produtos, criar_produto, editar_produto, deletar_produto, criar_segmento, adicionar_entrada, detalhar_produto, saida_estoque

urlpatterns = [
    path('', listar_produtos, name='listar_produtos'),
    path('criar/', criar_produto, name='criar_produto'),
    path('editar/<int:pk>/', editar_produto, name='editar_produto'),
    path('deletar/<int:pk>/', deletar_produto, name='deletar_produto'),
    path('segmento/criar/', criar_segmento, name='criar_segmento'),
    path('entrada/adicionar/<int:pk>/', adicionar_entrada, name='adicionar_entrada'), 
    path('detalhar/<int:pk>/', detalhar_produto, name='detalhar_produto'),  # URL para detalhar produto
    path('saida/<int:pk>/', saida_estoque, name='saida_estoque'),  # URL para saída de estoque
]

