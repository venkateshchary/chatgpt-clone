"""extension

Revision ID: 84bfc7df71c1
Revises: f8d97b1fc1b5
Create Date: 2026-11-07 17:17:34.190916

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import pgvector.sqlalchemy


# revision identifiers, used by Alembic.
revision: str = '84bfc7df71c1'
down_revision: Union[str, Sequence[str], None] = 'f8d97b1fc1b5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")

def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DROP EXTENSION IF EXISTS vector")
