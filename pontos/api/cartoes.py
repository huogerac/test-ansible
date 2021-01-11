from pontos.services import cartoes_services


def listar_cartoes():

    cartoes = cartoes_services.listar_cartoes()

    return {"data": cartoes}
