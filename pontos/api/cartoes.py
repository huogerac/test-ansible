from pontos.services import cartoes_services


def listar_cartoes():

    cartoes = cartoes_services.listar_cartoes()

    return {"data": cartoes}


def adicionar_ponto(cartao_id):
    return cartoes_services.adicionar_ponto(cartao_id)


def remover_ponto(cartao_id):
    return cartoes_services.remover_ponto(cartao_id)
