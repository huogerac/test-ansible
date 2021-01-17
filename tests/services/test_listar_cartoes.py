from pontos.services import cartoes_services
from tests.conftest import UsuarioFactory, EmpresaFactory, ProgramaFactory, CartaoFactory


def test_listar_lista_vazia(db_session):

    cartoes = cartoes_services.listar_cartoes(
        empresa_id=1,
        programa_id=1,
        page=1,
        page_size=100,
    )

    assert cartoes == []


def test_listar_cartoes(db_session):
    # Dado 10 cartoes cadastrados
    empresa = EmpresaFactory.create()
    pague10ganhe1 = ProgramaFactory.create(empresa_id=empresa.id)
    usuario = UsuarioFactory.create()
    cartao = CartaoFactory.create_batch(10, empresa_id=empresa.id, programa_id=pague10ganhe1.id, usuario_id=usuario.id)

    # Quando listamos os cartoes
    resultado = cartoes_services.listar_cartoes(
        empresa_id=empresa.id,
        programa_id=pague10ganhe1.id,
        page=1,
        page_size=100,
    )

    assert len(resultado) == 10
