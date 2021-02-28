from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views import View
from .models import Produto, Variacao
from django.forms.models import model_to_dict
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator



class ListagemProduto(ListView):
    queryset = Produto.objects.all().order_by("id")
    context_object_name = "produtos"
    paginate_by = 1
    pass


class DetalheProduto(DetailView):
    queryset = Produto.objects.all()
    template_name = "produto/detalhe.html"
    slug_url_kwarg = 'slug'


class AdicionarProduto(View):
    def post(self, *args, **kwargs):
        qtd = 1

        # if self.request.session.get("carrinho"):
        #     del self.request.session["carrinho"]
        #     self.request.session.save()

        variacao_id = self.request.POST.get("vid")
        if not variacao_id.isnumeric():
            messages.error(self.request, "teste")
            return redirect(self.request.META["HTTP_REFERER"])


        variacao = get_object_or_404(Variacao, id=variacao_id)

        if variacao.estoque < 1:
            messages.error(self.request,"Produto não disponível em estoque !")
            return redirect(self.request.META["HTTP_REFERER"])

        if not self.request.session.get("carrinho"):
            self.request.session["carrinho"] = {}
            self.request.session.save()

        if "qtd" in self.request.POST:
            qtd = self.request.POST.get('qtd')


        carrinho = self.request.session["carrinho"]

        produto = variacao.produto
        if variacao_id in carrinho:
            qtd = carrinho[variacao_id]["quantidade"] + 1
            if variacao.estoque < qtd:
                messages.warning(self.request,f"Estoque insuficiente {qtd}x do produto {produto.nome}, mas foram adicionados {variacao.estoque}x em seu carrinho.")
            carrinho[variacao_id]["quantidade"] = variacao.estoque
            carrinho[variacao_id]["preco_promo"] = variacao.estoque * variacao.preco_promo
            carrinho[variacao_id]["preco"] = variacao.estoque * variacao.preco
            carrinho[variacao_id]["preco_unitario_promo"] = variacao.preco_promo
            carrinho[variacao_id]["preco_unitario"] = variacao.preco
        else:
            carrinho[variacao_id] = get_dict_carrinho(variacao,produto)

        messages.success(self.request,"Produto foi adicionado ao seu carrinho!")
        self.request.session["carrinho"] = carrinho
        return redirect(self.request.META["HTTP_REFERER"])


class RemoverProduto(ListView):
    def get(self,*args,**kwargs):
        try:
            if self.request.session.get("carrinho"):
                del self.request.session["carrinho"][str(kwargs["id_variacao"])]
                self.request.session.save()

            if str(kwargs["id_variacao"]) not in self.request.session["carrinho"]:
                messages.success(self.request, "Produto removido do carrinho, o seu carrinho ficou vazio, adicione algo ao carrinho !")
                return redirect("listagem-produto")
            messages.success(self.request, "Produto removido do carrinho !")
        except Exception as e:
            print(e)
            messages.error(self.request, "Ocorreu um erro ao remover o produto do carrinho!")
        return redirect(self.request.META["HTTP_REFERER"])

class Carrinho(ListView):
    def get(self, *args, **kwargs):
        carrinho = self.request.session.get("carrinho", {})
        return render(self.request, "produto/carrinho.html",{"carrinho":carrinho})


class FinalizarCarrinho(View): 
    @method_decorator(login_required(login_url='/login/')) 
    def get(self, request, *args, **kwargs):
        
        dict_finalizar_carrinho = {
            "usuario": self.request.user,
            "carrinho": self.request.session["carrinho"]
        }
        return render(request, "produto/finalizar_carrinho.html", dict_finalizar_carrinho)

def get_dict_carrinho(variacao, produto):
    return {"img":produto.img.name ,"quantidade":1, "preco_promo":variacao.preco_promo, "preco":variacao.preco,"nome_variacao":variacao.nome,"preco_unitario_promo":variacao.preco_promo,"preco_unitario":variacao.preco,"id_variacao":variacao.pk,"nome_produto":produto.nome,"slug":produto.slug}