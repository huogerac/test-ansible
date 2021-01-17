from werkzeug.security import generate_password_hash

from pontos.ext.database import db
from pontos.models.usuarios import Usuario
from pontos.models.cartoes import Empresa, EmpresaGerente


def criar_usuario(nome_completo, fone, email, password, perfil="cliente", empresa_id=None):
    # pylint: disable=R0913
    if Usuario.query.filter_by(email=email).first():
        raise RuntimeError("Email já cadastrado")

    if Usuario.query.filter_by(fone=fone).first():
        raise RuntimeError("Fone já cadastrado")

    if perfil == "gerente" and not empresa_id:
        raise RuntimeError("Empresa-id é obrigatório para perfil de gerente")

    if perfil == "gerente":
        if not Empresa.query.filter_by(id=empresa_id).first():
            raise RuntimeError("Empresa ID inválido")

    password_hash = generate_password_hash(password)

    novo_usuario = Usuario(
        nome_completo=nome_completo,
        fone=fone,
        email=email,
        password=password_hash,
    )
    db.session.add(novo_usuario)
    db.session.commit()

    if perfil == "gerente":
        perfil_do_usuario = EmpresaGerente(
            empresa_id=empresa_id,
            usuario_id=novo_usuario.id,
            perfil=perfil,
        )
        db.session.add(perfil_do_usuario)

    db.session.commit()

    return novo_usuario.to_dict()


def obter_usuario_por_email_ou_none(email):
    return Usuario.query.filter_by(email=email).first()
