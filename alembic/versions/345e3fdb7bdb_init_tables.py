"""init tables

Revision ID: 345e3fdb7bdb
Revises: 
Create Date: 2026-06-03 16:25:45.798105
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "345e3fdb7bdb"
down_revision: Union[str, Sequence[str], None] = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # =========================
    # PLAYER TABLE
    # =========================
    op.create_table(
        "player",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("gold", sa.Integer, nullable=False, server_default=sa.text("100")),
        sa.Column("hp", sa.Integer, nullable=False, server_default=sa.text("100")),
        sa.Column("level", sa.Integer, nullable=False, server_default=sa.text("1")),
        sa.Column("xp", sa.Integer, nullable=False, server_default=sa.text("0")),
    )

    # =========================
    # SHOP TABLE
    # =========================
    op.create_table(
        "shop",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("itemName", sa.Text, nullable=False, unique=True),
        sa.Column("stock", sa.Integer, nullable=False),
        sa.Column("price", sa.Integer, nullable=False),
    )

    # =========================
    # PLAYER ITEMS TABLE
    # =========================
    op.create_table(
        "playerItems",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("playerID", sa.Integer, sa.ForeignKey("player.id"), nullable=False),
        sa.Column("itemName", sa.Text, sa.ForeignKey("shop.itemName"), nullable=False),
        sa.Column("quantity", sa.Integer, nullable=False),
        sa.UniqueConstraint("playerID", "itemName", name="uq_player_item"),
    )


def downgrade() -> None:
    op.drop_table("playerItems")
    op.drop_table("shop")
    op.drop_table("player")