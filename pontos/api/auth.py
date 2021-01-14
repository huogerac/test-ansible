from pontos.services import auth_services
from pontos.services import token_services


def signin(body):
    usuario = auth_services.authenticate(email=body["email"], password=body["password"])
    return {
        "usuario": usuario.to_dict(),
        "token": token_services.generate_token(usuario, days=7),
    }
