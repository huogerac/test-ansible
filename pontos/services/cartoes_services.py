from datetime import datetime, timezone
from sqlalchemy import func
from sqlalchemy.orm.exc import NoResultFound

from pontos.exceptions import NotFoundException, InvalidValueException
from pontos.ext.database import db
from pontos.models.cartoes import Cartao, Ponto
from pontos.models.usuarios import Usuario


def listar_cartoes(empresa_id, programa_id, page, page_size, token_info=None):

    pontos_ativos = (
        db.session.query(Ponto.cartao_id.label("cartao_id"), func.count(Ponto.cartao_id).label("total"))
        .group_by(Ponto.cartao_id)
        .filter(Ponto.removido_em == None)
        .subquery("pontos_ativos")
    )

    qs = (
        db.session.query(
            Cartao.id,
            Cartao.empresa_id,
            Cartao.programa_id,
            Usuario.id,
            Usuario.nome_completo,
            Usuario.fone,
            Usuario.email,
            Usuario.avatar,
            Usuario.criado_em,
            pontos_ativos.c.total,
        )
        .join(Usuario)
        .join(pontos_ativos, pontos_ativos.c.cartao_id == Cartao.id, isouter=True)
    )

    if token_info["perfil"] == "gerente":
        qs = qs.filter(Cartao.empresa_id == token_info["empresa_id"])
    elif token_info["perfil"] == "cliente":
        usuario_id = token_info["sub"]
        qs = qs.filter(Cartao.usuario_id == usuario_id)

    return [
        {
            "id": c_id,
            "empresa_id": e_id,
            "programa_id": p_id,
            "usuario": {
                "id": u_id,
                "nome_completo": nome,
                "fone": fone,
                "email": email,
                "avatar": avatar,
                "criado_em": criado_em.isoformat(),
            },
            "pontos": pontos if pontos else 0,
        }
        for (c_id, e_id, p_id, u_id, nome, fone, email, avatar, criado_em, pontos) in qs
    ]


def _obtem_pontos_do_cartao(cartao_id):
    try:
        _, pontos = (
            db.session.query(Ponto.cartao_id, func.count(Ponto.cartao_id))
            .group_by(Ponto.cartao_id)
            .filter(Ponto.cartao_id == cartao_id)
            .filter(Ponto.removido_em == None)
            .one()
        )
        return pontos
    except NoResultFound:
        return 0


def adicionar_ponto(cartao_id):
    """ Adiciona 1 ponto ao cartao"""
    try:
        cartao = Cartao.query.filter(Cartao.id == cartao_id).one()
        usuario = Usuario.query.filter(Usuario.id == cartao.usuario_id).one()

        novo_ponto = Ponto(cartao_id=cartao.id)
        db.session.add(novo_ponto)
        db.session.commit()

        pontos = _obtem_pontos_do_cartao(cartao_id)

        return {
            "id": cartao.id,
            "empresa_id": cartao.empresa_id,
            "programa_id": cartao.programa_id,
            "usuario": usuario.to_dict(),
            "pontos": pontos,
        }

    except NoResultFound:
        raise CartaoNaoEcontrado(cartao_id)


def remover_ponto(cartao_id):
    """ Remove 1 ponto do cartao"""
    try:
        cartao = Cartao.query.filter(Cartao.id == cartao_id).one()
        usuario = Usuario.query.filter(Usuario.id == cartao.usuario_id).one()

        ponto = Ponto.query.filter(Ponto.cartao_id == cartao_id).filter(Ponto.removido_em == None).first()
        if ponto is None:
            raise InvalidValueException("Cartão ID: {} não tem ponto para ser removido".format(cartao_id))

        ponto.removido_em = datetime.now(timezone.utc)
        db.session.add(ponto)
        db.session.commit()

        pontos = _obtem_pontos_do_cartao(cartao_id)

        return {
            "id": cartao.id,
            "empresa_id": cartao.empresa_id,
            "programa_id": cartao.programa_id,
            "usuario": usuario.to_dict(),
            "pontos": pontos,
        }

    except NoResultFound:
        raise CartaoNaoEcontrado(cartao_id)


class CartaoNaoEcontrado(NotFoundException):
    def __init__(self, cartao_id):
        super().__init__(f"Cartão ID: '{cartao_id}' não encontrado")
