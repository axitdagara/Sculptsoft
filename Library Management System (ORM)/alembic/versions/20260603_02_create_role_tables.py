

"""Create roles and user_roles tables

Revision ID: 20260603_02
Revises: 20260526_01
Create Date: 2026-06-03 00:00:00
"""

from alembic import op
import sqlalchemy as sa


revision = "20260603_02"
down_revision = "20260526_01"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "roles",
        sa.Column("role_id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("name", sa.String(length=50), nullable=False),
        sa.UniqueConstraint("name", name="uq_roles_name"),
    )

    op.create_table(
        "user_roles",
        sa.Column("user_role_id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False),
        sa.Column("role_id", sa.Integer(), sa.ForeignKey("roles.role_id", ondelete="CASCADE"), nullable=False),
        sa.UniqueConstraint("user_id", "role_id", name="uq_user_roles_user_id_role_id"),
    )

    op.execute("INSERT INTO roles (name) VALUES ('admin'), ('user')")
    op.execute(
        """
        INSERT INTO user_roles (user_id, role_id)
        SELECT users.user_id, roles.role_id
        FROM users
        JOIN roles ON roles.name = 'user'
        """
    )


def downgrade() -> None:
    op.drop_table("user_roles")
    op.drop_table("roles")
