"""player table

Revision ID: 26633e558bdf
Revises: 345e3fdb7bdb
Create Date: 2026-06-04 17:25:51.195243
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '26633e558bdf'
down_revision: Union[str, Sequence[str], None] = '345e3fdb7bdb'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Upgrade schema."""

    # ONLY SAFE ALTERATIONS (NO DROPS)

    op.alter_column(
        'player', 'gold',
        existing_type=sa.INTEGER(),
        nullable=True,
        existing_server_default=sa.text('100')
    )

    op.alter_column(
        'player', 'hp',
        existing_type=sa.INTEGER(),
        nullable=True,
        existing_server_default=sa.text('100')
    )

    op.alter_column(
        'player', 'level',
        existing_type=sa.INTEGER(),
        nullable=True,
        existing_server_default=sa.text('1')
    )

    op.alter_column(
        'player', 'xp',
        existing_type=sa.INTEGER(),
        nullable=True,
        existing_server_default=sa.text('0')
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.alter_column(
        'player', 'xp',
        existing_type=sa.INTEGER(),
        nullable=False,
        existing_server_default=sa.text('0')
    )

    op.alter_column(
        'player', 'level',
        existing_type=sa.INTEGER(),
        nullable=False,
        existing_server_default=sa.text('1')
    )

    op.alter_column(
        'player', 'hp',
        existing_type=sa.INTEGER(),
        nullable=False,
        existing_server_default=sa.text('100')
    )

    op.alter_column(
        'player', 'gold',
        existing_type=sa.INTEGER(),
        nullable=False,
        existing_server_default=sa.text('100')
    )