from werkzeug.security import check_password_hash

from pontos.services import usuarios_services
from pontos.exceptions import UnauthorizedException


def authenticate(email, password):
    usuario = usuarios_services.obter_usuario_por_email_ou_none(email)
    senha_valida = check_password_hash(usuario.password, password)

    if usuario is None or not senha_valida:
        raise UnauthorizedException("Email ou senha inválida")

    return usuario
