from contextlib import asynccontextmanager

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import session, get_db
from app.models import User
from app.repositories import ConversationRepository, MessageRepository, UserRepository
from app.services.chat_service import ChatService
from app.llm import OllamaClient


def get_user_repo(db: AsyncSession = Depends(get_db)) -> UserRepository:
    return UserRepository(db)


def get_conversation_repo(db: AsyncSession = Depends(get_db)) -> ConversationRepository:
    return ConversationRepository(db)


def get_message_repo(db: AsyncSession = Depends(get_db)) -> MessageRepository:
    return MessageRepository(db)


# @asynccontextmanager
# async def _fresh_repos():
#     async with SessionLocal() as session:
#         yield ConversationRepository(session), MessageRepository(session)


def get_chat_service(
    conversations: ConversationRepository = Depends(get_conversation_repo),
    messages: MessageRepository = Depends(get_message_repo),
) -> ChatService:
    return ChatService(conversations, messages, OllamaClient(), _fresh_repos)


# Temporary auth stub: everything runs as one dev user until JWT auth is added.
async def get_current_user(users: UserRepository = Depends(get_user_repo)) -> User:
    user = await users.get_by_email("dev@local")
    return user or await users.create("dev@local", "not-a-real-hash")
