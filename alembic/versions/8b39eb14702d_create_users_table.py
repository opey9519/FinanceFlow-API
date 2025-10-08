"""create users table

Revision ID: 8b39eb14702d
Revises: 00e60a73d62f
Create Date: 2025-10-08 14:50:21.112478

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8b39eb14702d'
down_revision: Union[str, Sequence[str], None] = '00e60a73d62f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
