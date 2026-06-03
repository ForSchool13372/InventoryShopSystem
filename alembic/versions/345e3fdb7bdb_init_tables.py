"""init tables

Revision ID: 345e3fdb7bdb
Revises: 
Create Date: 2026-06-03 16:25:45.798105
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '345e3fdb7bdb'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "player",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("gold", sa.Integer, nullable=False, server_default="100"),
        sa.Column("hp", sa.Integer, nullable=False, server_default="100"),
        sa.Column("level", sa.Integer, nullable=False, server_default="1"),
        sa.Column("xp", sa.Integer, nullable=False, server_default="0"),
    )

    op.create_table(
        "shop",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("itemName", sa.Text, nullable=False, unique=True),
        sa.Column("stock", sa.Integer, nullable=False),
        sa.Column("price", sa.Integer, nullable=False),
    )

    op.create_table(
        "playerItems",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("playerID", sa.Integer, nullable=False),
        sa.Column("itemName", sa.Text, nullable=False),
        sa.Column("quantity", sa.Integer, nullable=False),
        sa.UniqueConstraint("playerID", "itemName"),
    )


def downgrade() -> None:
    op.drop_table("playerItems")
    op.drop_table("shop")
    op.drop_table("player")