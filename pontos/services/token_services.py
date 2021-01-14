import jwt
from jwt.exceptions import InvalidTokenError
from datetime import datetime, timezone, timedelta
from flask import current_app

from pontos.exceptions import UnauthorizedException


def generate_token(user, days=0, hours=0):
    perfil, empresa_id = user.perfil
    return jwt.encode(
        {
            "iss": "http://fi.com",
            "aud": "uniquenumber.fi.com",
            "exp": datetime.now(timezone.utc) + timedelta(days=days, hours=hours),
            "sub": user.id,
            "email": user.email,
            "name": user.nome_completo,
            "fone": user.fone,
            "perfil": perfil,
            "empresa_id": empresa_id,
        },
        current_app.config["SECRET_KEY"],
        algorithm="HS256",
    )


def decode_token(token):
    try:
        result = jwt.decode(
            jwt=token,
            key=current_app.config["SECRET_KEY"],
            issuer="http://fi.com",
            audience="uniquenumber.fi.com",
            algorithms=["HS256"],
        )
        return result
    except InvalidTokenError as error:
        raise UnauthorizedException(str(error))
