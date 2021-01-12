from datetime import datetime, timezone
import sqlalchemy as sa

from pontos.ext.database import db


class Usuario(db.Model):

    __tablename__ = "usuarios"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    nome_completo = sa.Column(sa.String(128), nullable=False)
    fone = sa.Column(sa.String(32), nullable=False, unique=True)
    email = sa.Column(sa.String(255), nullable=False, unique=True)
    password = sa.Column(sa.String(128), nullable=False)
    avatar = sa.Column(sa.String(255), nullable=True)
    oauth_provider = sa.Column(sa.String(255), nullable=True)
    oauth_id = sa.Column(sa.String(255), nullable=True)
    criado_em = sa.Column(sa.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return "{} ({})".format(self.nome_completo, self.fone)

    def to_dict(self):
        return {
            "id": self.id,
            "nome_completo": self.nome_completo,
            "fone": self.fone,
            "email": self.email,
            "avatar": self.avatar,
            "criado_em": self.criado_em.isoformat(),
        }