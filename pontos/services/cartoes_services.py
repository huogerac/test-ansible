from pontos.ext.database import db
from pontos.models.cartoes import Cartao
from pontos.models.usuarios import Usuario


def listar_cartoes():

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
        )
        .join(Usuario)
        .all()
    )

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
            "pontos": 2,
        }
        for (c_id, e_id, p_id, u_id, nome, fone, email, avatar, criado_em) in qs
    ]