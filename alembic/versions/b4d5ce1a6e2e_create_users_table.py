"""create users table

Revision ID: b4d5ce1a6e2e
Revises: 8b39eb14702d
Create Date: 2025-10-08 14:54:00.818087

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b4d5ce1a6e2e'
down_revision: Union[str, Sequence[str], None] = '8b39eb14702d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
