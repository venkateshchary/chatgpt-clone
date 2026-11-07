from app.db.session import Base
from app.core.config import settings
import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Boolean, String, ForeignKey, Float, Text
from datetime import datetime
from app.dependencies.uuid_gen import _uuid
from .user import User


class UserSettings(Base):
    __tablename__ = "user_settings"
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    model: Mapped[str] = mapped_column(String(100), default=settings.default_model)
    temperature: Mapped[float] = mapped_column(Float, default=0.7)
    system_prompt: Mapped[str] = mapped_column(Text, default="You are a helpful assistant.")
    theme: Mapped[str] = mapped_column(String(20), default="system")
    memory_enabled: Mapped[bool] = mapped_column(Boolean, default=True)

    user: Mapped[User] = relationship(back_populates="settings")
