from django.shortcuts import redirect, render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views import View
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from produto.models import Variacao
from .models import Pedido, ItemPedido



class DispatchLoginRequired(View):
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect(reverse_lazy("login"))

        return super().dispatch(request, *args, **kwargs)

class PagarPedido(DispatchLoginRequired, DetailView):
    template_name = "pedido/pagar_pedido.html"
    model = Pedido
    pk_url_kwarg = "pk" 
    context_object_name = "pedido"
    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset()
        return queryset.filter(usuario=self.request.user)
        

class FinalizarPedido(View):
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
        
        qtd_total_carrinho = sum((cart["quantidade"] for cart in carrinho.values()))
        valor_total_carrinho = sum([item["preco_promo"] if item["preco_promo"] else item["preco"] for key,item in carrinho.items()])
        
      
        pedido = Pedido(
            user=self.request.user,
            total=valor_total_carrinho,
            qtd_total=qtd_total_carrinho,
            status="C"
        )
        pedido.save()
        ItemPedido.objects.bulk_create(
            [
                ItemPedido(**{"pedido":pedido, "produto":item["nome_produto"], "variacao":item["nome_variacao"], "id_variacao":item["id_variacao"], "preco_promo":item["preco_promo"], "preco":item["preco"], "quantidade":item["quantidade"], "imagem":item["img"] }) for item in carrinho.values()
            ]
        )
       
        """dict_pagar = {
            "qtd_total_carrinho":qtd_total_carrinho,
            "valor_total_carrinho":valor_total_carrinho
        }"""
        del self.request.session["carrinho"]
        
        return redirect(
            reverse('pagar-pedido', kwargs={'pk':pedido.pk}) 
        )
        #return render(self.request, self.template_name, dict_pagar)

class DetalhePedido(ListView):
    pass

class ListaPedido(ListView):
    pass