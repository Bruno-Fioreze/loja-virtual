from django.urls import path, include
from .views import PagarPedido, DetalhePedido, FinalizarPedido, ListaPedido

urlpatterns = [
    path("pagar-perdido/<int:pk>/", PagarPedido.as_view(), name="pagar-pedido"),
    path("finalizar-pedido/", FinalizarPedido.as_view(), name="finalizar-pedido"),
    path("detalhe-pedido/", DetalhePedido.as_view(), name="detalhe-pedido"),
    path("lista-pedido/", ListaPedido.as_view(), name="lista-pedido"),
]