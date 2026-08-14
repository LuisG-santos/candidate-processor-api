"""add candidate server defaults

Revision ID: 0e869f2d161d
Revises: c2d9540686c6
Create Date: 2026-08-14 11:25:16.862690

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0e869f2d161d'
down_revision: Union[str, Sequence[str], None] = 'c2d9540686c6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column(
        "candidates",
        "id",
        server_default=sa.text("gen_random_uuid()"),
    )

    op.alter_column(
        "candidates",
        "created_at",
        server_default=sa.text("CURRENT_TIMESTAMP"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column(
        "candidates",
        "id",
        server_default=None,
    )

    op.alter_column(
        "candidates",
        "created_at",
        server_default=None,
    )
