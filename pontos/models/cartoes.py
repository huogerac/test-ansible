from datetime import datetime, timezone
import sqlalchemy as sa

from pontos.ext.database import db
from pontos.models.usuarios import Usuario


class Empresa(db.Model):

    __tablename__ = "empresas"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    nome = sa.Column(sa.String(128), nullable=False, unique=True)
    criado_em = sa.Column(sa.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return "{} ({})".format(self.nome, self.id)


class EmpresaGerente(db.Model):

    __tablename__ = "empresagerentes"

    PERFILS = ("gerente", "cliente")

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    empresa_id = sa.Column(
        sa.Integer,
        sa.ForeignKey("empresas.id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    usuario_id = sa.Column(
        sa.Integer,
        sa.ForeignKey("usuarios.id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    perfil = sa.Column(sa.Enum(*PERFILS, name="perfil_usuario", default="cliente"))

    usuario = db.relationship(Usuario, backref=db.backref("empresas", lazy="dynamic"))


class Programa(db.Model):

    __tablename__ = "programas"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    empresa_id = sa.Column(
        sa.Integer,
        sa.ForeignKey("empresas.id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    nome = sa.Column(sa.String(128), nullable=False, unique=True)
    total_pontos = sa.Column(sa.Integer, default=10)
    criado_em = sa.Column(sa.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    empresa = db.relationship(Empresa, backref=db.backref("programas", lazy="dynamic"))

    def __repr__(self):
        return self.nome


class Cartao(db.Model):
    __tablename__ = "cartoes"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    empresa_id = sa.Column(
        sa.Integer,
        sa.ForeignKey("empresas.id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    programa_id = sa.Column(
        sa.Integer,
        sa.ForeignKey("programas.id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    usuario_id = sa.Column(
        sa.Integer,
        sa.ForeignKey("usuarios.id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    criado_em = sa.Column(sa.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    premiado_em = sa.Column(sa.DateTime(timezone=True), nullable=True)
    resgatado_em = sa.Column(sa.DateTime(timezone=True), nullable=True)

    empresa = db.relationship(Empresa, backref=db.backref("cartoes", lazy="dynamic"))
    programa = db.relationship(Programa, backref=db.backref("cartoes", lazy="dynamic"))
    usuario = db.relationship(Usuario, backref=db.backref("cartoes", lazy="dynamic"))

    def __repr__(self):
        return "Cartao {}".format(self.id)


class Ponto(db.Model):
    __tablename__ = "pontos"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    cartao_id = sa.Column(
        sa.Integer,
        sa.ForeignKey("cartoes.id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    criado_em = sa.Column(sa.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    removido_em = sa.Column(sa.DateTime(timezone=True), nullable=True)
