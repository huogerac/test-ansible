from pontos.services import cartoes_services


def listar_cartoes(empresa_id=None, programa_id=None, page=1, page_size=500, token_info=None):
    cartoes = cartoes_services.listar_cartoes(empresa_id, programa_id, page, page_size, token_info)
    return {"data": cartoes}


def adicionar_ponto(cartao_id, token_info=None):
    return cartoes_services.adicionar_ponto(cartao_id)


def remover_ponto(cartao_id, token_info=None):
    return cartoes_services.remover_ponto(cartao_id)


def utilizar_pontos(cartao_id, token_info=None):
    return cartoes_services.utilizar_pontos(cartao_id), 201
