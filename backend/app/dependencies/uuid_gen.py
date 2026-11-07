from sqlalchemy.orm import Mapped, mapped_column
import uuid
from sqlalchemy.dialects.postgresql import UUID


def _uuid():
    return mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
