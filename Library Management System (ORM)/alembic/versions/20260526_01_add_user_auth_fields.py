"""Add password hash and unique user names

Revision ID: 20260526_01
Revises: 20260525_01
Create Date: 2026-05-26 00:00:00
"""

from alembic import op
import sqlalchemy as sa


revision = "20260526_01"
down_revision = "20260525_01"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("users", sa.Column("password_hash", sa.String(length=255), nullable=True))
    op.create_unique_constraint("uq_users_name", "users", ["name"])


def downgrade() -> None:
    op.drop_constraint("uq_users_name", "users", type_="unique")
    op.drop_column("users", "password_hash")