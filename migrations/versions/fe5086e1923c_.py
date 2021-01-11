"""empty message

Revision ID: fe5086e1923c
Revises: 
Create Date: 2021-01-11 14:33:43.951672

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "fe5086e1923c"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "empresas",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("nome", sa.String(length=128), nullable=False),
        sa.Column("criado_em", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("nome"),
    )
    op.create_table(
        "usuarios",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("nome_completo", sa.String(length=128), nullable=False),
        sa.Column("fone", sa.String(length=32), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("password", sa.String(length=128), nullable=False),
        sa.Column("avatar", sa.String(length=255), nullable=True),
        sa.Column("oauth_provider", sa.String(length=255), nullable=True),
        sa.Column("oauth_id", sa.String(length=255), nullable=True),
        sa.Column("criado_em", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
        sa.UniqueConstraint("fone"),
    )
    op.create_table(
        "programas",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("empresa_id", sa.Integer(), nullable=False),
        sa.Column("nome", sa.String(length=128), nullable=False),
        sa.Column("total_pontos", sa.Integer(), nullable=True),
        sa.Column("criado_em", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["empresa_id"], ["empresas.id"], onupdate="CASCADE", ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("nome"),
    )
    op.create_index(op.f("ix_programas_empresa_id"), "programas", ["empresa_id"], unique=False)
    op.create_table(
        "cartoes",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("empresa_id", sa.Integer(), nullable=False),
        sa.Column("programa_id", sa.Integer(), nullable=False),
        sa.Column("usuario_id", sa.Integer(), nullable=False),
        sa.Column("criado_em", sa.DateTime(timezone=True), nullable=True),
        sa.Column("premiado_em", sa.DateTime(timezone=True), nullable=True),
        sa.Column("resgatado_em", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["empresa_id"], ["empresas.id"], onupdate="CASCADE", ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["programa_id"], ["programas.id"], onupdate="CASCADE", ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["usuario_id"], ["usuarios.id"], onupdate="CASCADE", ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_cartoes_empresa_id"), "cartoes", ["empresa_id"], unique=False)
    op.create_index(op.f("ix_cartoes_programa_id"), "cartoes", ["programa_id"], unique=False)
    op.create_index(op.f("ix_cartoes_usuario_id"), "cartoes", ["usuario_id"], unique=False)
    op.create_table(
        "pontos",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("cartao_id", sa.Integer(), nullable=False),
        sa.Column("criado_em", sa.DateTime(timezone=True), nullable=True),
        sa.Column("removido_em", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["cartao_id"], ["cartoes.id"], onupdate="CASCADE", ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_pontos_cartao_id"), "pontos", ["cartao_id"], unique=False)


def downgrade():

    op.drop_index(op.f("ix_pontos_cartao_id"), table_name="pontos")
    op.drop_table("pontos")
    op.drop_index(op.f("ix_cartoes_usuario_id"), table_name="cartoes")
    op.drop_index(op.f("ix_cartoes_programa_id"), table_name="cartoes")
    op.drop_index(op.f("ix_cartoes_empresa_id"), table_name="cartoes")
    op.drop_table("cartoes")
    op.drop_index(op.f("ix_programas_empresa_id"), table_name="programas")
    op.drop_table("programas")
    op.drop_table("usuarios")
    op.drop_table("empresas")
