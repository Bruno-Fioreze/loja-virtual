from django.urls import path, include
from .views import ListagemProduto, DetalheProduto, RemoverProduto, Carrinho, FinalizarProduto,AdicionarProduto

urlpatterns = [
    path("", ListagemProduto.as_view(), name="listagem-produto"),
    path("carrinho/", Carrinho.as_view(), name="carrinho"),
    path("adicionar-carrinho/", AdicionarProduto.as_view(), name="adicionar-carrinho"),
    path("remover-carrinho/<int:id_variacao>/", RemoverProduto.as_view(), name="remover-carrinho"),
    path("finalizar-carrinho/", FinalizarProduto.as_view(), name="finalizar-carrinho"),
    path("<slug>", DetalheProduto.as_view(), name="detalhe-produto"),
]





