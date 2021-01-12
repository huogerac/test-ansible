import os
import pytest
import sqlalchemy as sa
import factory
from sqlalchemy.orm import Session

from pontos.app import create_app
from pontos.ext.database import db
from pontos.models.cartoes import Empresa, Programa, Cartao
from pontos.models.usuarios import Usuario


@pytest.fixture(scope="session")
def app():
    os.environ["FLASK_ENV"] = "testing"
    app = create_app()
    with app.app_context():
        db.create_all(app=app)
        yield app
        db.drop_all(app=app)


@pytest.fixture(scope="function", autouse=True)
def db_session(app):
    conn = db.engine.connect()
    trans = conn.begin()

    session = Session(bind=conn)
    session.begin_nested()

    # then each time that SAVEPOINT ends, reopen it
    @sa.event.listens_for(db.session, "after_transaction_end")
    def restart_savepoint(session, transaction):
        if transaction.nested and not transaction._parent.nested:
            session.expire_all()
            session.begin_nested()

    db.session.begin_nested()

    UsuarioFactory._meta.sqlalchemy_session = db.session
    EmpresaFactory._meta.sqlalchemy_session = db.session
    ProgramaFactory._meta.sqlalchemy_session = db.session
    CartaoFactory._meta.sqlalchemy_session = db.session

    yield db.session

    # rollback everything
    trans.rollback()
    conn.close()
    db.session.remove()


class UsuarioFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Usuario

    id = factory.Sequence(int)
    nome_completo = factory.Faker("name")
    password = "pass"
    fone = factory.Faker("phone_number")
    email = factory.Faker("ascii_email")
    criado_em = factory.Faker("date_time")


class EmpresaFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Empresa

    id = factory.Sequence(int)
    nome = factory.Sequence(lambda n: "empresa-{}".format(n))
    criado_em = factory.Faker("date_time")


class ProgramaFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Programa

    id = factory.Sequence(int)
    empresa_id = 1
    nome = factory.Sequence(lambda n: "programa-{}".format(n))
    total_pontos = 10
    criado_em = factory.Faker("date_time")


class CartaoFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Cartao

    id = factory.Sequence(int)
    empresa_id = 1
    programa_id = 1
    usuario_id = 1
    criado_em = factory.Faker("date_time")
