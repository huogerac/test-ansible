"""Adiciona tabela de gerentes de empresas

Revision ID: b6821fc50e2f
Revises: fe5086e1923c
Create Date: 2021-01-14 14:08:57.870758

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "b6821fc50e2f"
down_revision = "fe5086e1923c"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "empresagerentes",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("empresa_id", sa.Integer(), nullable=False),
        sa.Column("usuario_id", sa.Integer(), nullable=False),
        sa.Column("perfil", sa.Enum("gerente", "cliente", name="perfil_usuario"), nullable=True),
        sa.ForeignKeyConstraint(["empresa_id"], ["empresas.id"], onupdate="CASCADE", ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["usuario_id"], ["usuarios.id"], onupdate="CASCADE", ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_empresagerentes_empresa_id"), "empresagerentes", ["empresa_id"], unique=False)
    op.create_index(op.f("ix_empresagerentes_usuario_id"), "empresagerentes", ["usuario_id"], unique=False)


def downgrade():
    op.drop_index(op.f("ix_empresagerentes_usuario_id"), table_name="empresagerentes")
    op.drop_index(op.f("ix_empresagerentes_empresa_id"), table_name="empresagerentes")
    op.drop_table("empresagerentes")
