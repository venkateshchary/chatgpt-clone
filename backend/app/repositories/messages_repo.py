import uuid

from sqlalchemy import select

from app.models import Message
from .base import BaseRepository


class MessageRepository(BaseRepository[Message]):
    model = Message

    async def create(self, conversation_id: uuid.UUID, role: str, content: str) -> Message:
        return await self.add(Message(conversation_id=conversation_id, role=role, content=content))

    async def list_for_conversation(self, conversation_id: uuid.UUID) -> list[Message]:
        q = select(Message).where(Message.conversation_id == conversation_id).order_by(Message.created_at)
        return list((await self.session.execute(q)).scalars().all())

    async def recent(self, conversation_id: uuid.UUID, limit: int) -> list[Message]:
        """Last `limit` messages, oldest first."""
        q = (
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(Message.created_at.desc())
            .limit(limit)
        )
        return list((await self.session.execute(q)).scalars().all())[::-1]
