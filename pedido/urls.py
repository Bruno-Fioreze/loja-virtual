from django.urls import path, include
from .views import PagarPedido, DetalhePedido, FinalizarPedido

urlpatterns = [
    path("pagar-perdido", PagarPedido, name="pagar-pedido"),
    path("finalizar-pedido", FinalizarPedido, name="finalizar-pedido"),
    path("detalhe-pedido", DetalhePedido, name="detalhe-pedido"),
]