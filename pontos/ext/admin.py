from flask_admin import Admin
from flask_admin.contrib import sqla
from flask_basicauth import BasicAuth
from flask import redirect, Response
from werkzeug.exceptions import HTTPException

from pontos.ext.database import db
from pontos.models.cartoes import Empresa, Programa, Cartao, Ponto
from pontos.models.usuarios import Usuario

admin = Admin()
basic_auth = BasicAuth()


def init_app(app):
    basic_auth.init_app(app)
    admin.init_app(app)
    admin.add_view(EmpresaModelView(Empresa, db.session, category="Cartões"))
    admin.add_view(ProtectedModelView(Programa, db.session, category="Cartões"))
    admin.add_view(ProtectedModelView(Cartao, db.session, category="Cartões"))
    admin.add_view(ProtectedModelView(Ponto, db.session, category="Cartões"))
    admin.add_view(ProtectedModelView(Usuario, db.session, category="Usuários"))


class AuthException(HTTPException):
    def __init__(self, message):
        super().__init__(message, Response(message, 401, {"WWW-Authenticate": 'Basic realm="Login Required"'}))


class ProtectedModelView(sqla.ModelView):
    def is_accessible(self):
        if not basic_auth or not basic_auth.authenticate():
            raise AuthException("Not authenticated.")
        return True

    def inaccessible_callback(self, name, **kwargs):
        return redirect(basic_auth.challenge())


class EmpresaModelView(ProtectedModelView):
    column_list = "id nome criado_em".split()
    column_filters = "nome criado_em".split()
    can_delete = True
    can_export = True


class ProgramaModelView(ProtectedModelView):
    column_list = "id empresa_id nome total_pontos criado_em".split()
    column_filters = "empresa_id nome criado_em".split()
    can_delete = True
    can_export = True
