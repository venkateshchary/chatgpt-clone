import uuid

from sqlalchemy import select

from app.models import Conversation
from .base import BaseRepository


class ConversationRepository(BaseRepository[Conversation]):
    model = Conversation

    async def get_for_user(self, conv_id: uuid.UUID, user_id: uuid.UUID) -> Conversation | None:
        q = select(Conversation).where(Conversation.id == conv_id, Conversation.user_id == user_id)
        return (await self.session.execute(q)).scalar_one_or_none()

    async def list_for_user(self, user_id: uuid.UUID) -> list[Conversation]:
        q = select(Conversation).where(Conversation.user_id == user_id).order_by(Conversation.updated_at.desc())
        return list((await self.session.execute(q)).scalars().all())

    async def create(self, user_id: uuid.UUID, title: str = "New chat") -> Conversation:
        return await self.add(Conversation(user_id=user_id, title=title))

    async def set_title(self, conv_id: uuid.UUID, title: str) -> None:
        conv = await self.get(conv_id)
        if conv:
            conv.title = title
            await self.session.commit()
