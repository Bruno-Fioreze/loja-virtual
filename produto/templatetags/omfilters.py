from django.template import Library

register = Library()

@register.filter
def formata_preco(valor):
    return f"R$ {valor:.2f}".replace(".",",")


@register.filter
def qtd_carrinho(carrinho):
    return sum((cart["quantidade"] for cart in carrinho.values()))


@register.filter
def valor_total_carrinho(carrinho):

    total = [
            item["preco_promo"] if item["preco_promo"] else item["preco"] for key,item in carrinho.items()
        ]

    return sum(
        total
    )
