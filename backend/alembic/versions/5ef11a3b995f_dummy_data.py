"""dummy data

Revision ID: 5ef11a3b995f
Revises: 84bfc7df71c1
Create Date: 2026-11-07 17:23:01.336238

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import pgvector.sqlalchemy


# revision identifiers, used by Alembic.
revision: str = '5ef11a3b995f'
down_revision: Union[str, Sequence[str], None] = '84bfc7df71c1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass

def downgrade() -> None:
    """Downgrade schema."""
    pass
