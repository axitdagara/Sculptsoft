"""Create initial library tables

Revision ID: 20260525_01
Revises:
Create Date: 2026-05-25 00:00:00
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "20260525_01"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "books",
        sa.Column("book_id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("author", sa.String(length=255), nullable=False),
        sa.Column("available", sa.Boolean(), nullable=False, server_default=sa.text("true")),
    )

    op.create_table(
        "users",
        sa.Column("user_id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("borrow_limit", sa.Integer(), nullable=False, server_default="3"),
        sa.Column("borrow_days", sa.Integer(), nullable=False, server_default="14"),
        sa.Column("fine_per_day", sa.Numeric(10, 2), nullable=False, server_default="2.00"),
    )

    op.create_table(
        "borrow_history",
        sa.Column("history_id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False),
        sa.Column("book_id", sa.Integer(), sa.ForeignKey("books.book_id", ondelete="CASCADE"), nullable=False),
        sa.Column("borrowed_on", sa.Date(), nullable=False),
        sa.Column("due_on", sa.Date(), nullable=False),
        sa.Column("returned_on", sa.Date(), nullable=True),
        sa.Column("fine", sa.Numeric(10, 2), nullable=False, server_default="0.00"),
    )


def downgrade() -> None:
    op.drop_table("borrow_history")
    op.drop_table("users")
    op.drop_table("books")
