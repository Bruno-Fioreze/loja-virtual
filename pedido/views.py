from django.shortcuts import redirect, render
from django.views.generic.list import ListView
from django.views import View
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from produto.models import Variacao


class PagarPedido(View):
    template_name = "pedido/pagar_pedido.html"
    @method_decorator(login_required(login_url='/login/'))  
    def get(self,*args,**kwargs):

        if not self.request.session.get("carrinho"):
            messages.error(
                self.request,
                "Seu carrinho está vazio."
            )
            return redirect(reverse_lazy("listagem-produto"))
        
        estoque_insuficiente = False
        dict_pagar = {}

        carrinho = self.request.session.get("carrinho")
        carrinho_id = [variacao for variacao in carrinho]
        variacoes = list(Variacao.objects.select_related("produto").filter(id__in=carrinho_id))

        for variacao in variacoes:
            estoque_insuficiente = True
            qtd_variacao_estoque = variacao.estoque
            qtd_carrinho = carrinho[str(variacao.id)]["quantidade"]
            preco_unitario = carrinho[str(variacao.id)]["preco_unitario"]
            preco_unitario_promo = carrinho[str(variacao.id)]["preco_unitario_promo"]

            if qtd_variacao_estoque < qtd_carrinho:
                carrinho[str(variacao.id)]["quantidade"] = qtd_variacao_estoque
                carrinho[str(variacao.id)]["preco"] = qtd_variacao_estoque * preco_unitario
                carrinho[str(variacao.id)]["preco_promo"] = qtd_variacao_estoque * preco_unitario_promo

                               
        if estoque_insuficiente: 
            messages.error(self.request, "Quantidade de produtos do carrinho insuficiente, a quantidade foi substituida pela disponivel. ")
            self.request.session.save()
        return render(self.request, self.template_name, dict_pagar)

        
class FinalizarPedido(ListView):
    pass

class DetalhePedido(ListView):
    pass