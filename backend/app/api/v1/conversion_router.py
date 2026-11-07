import uuid

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse

from app.dependencies.deps import get_chat_service, get_conversation_repo, get_current_user, get_message_repo
from app.models import User
from app.repositories import ConversationRepository, MessageRepository
from app.schemas import ConversationOut, MessageOut, SendMessage
from app.services import ChatService

router = APIRouter(prefix="/conversations", tags=["conversations"])


# Define a clean resource prefix
router = APIRouter(prefix="/users", tags=["Users V1"])



@router.get("", response_model=list[ConversationOut])
async def list_conversations(
    user: User = Depends(get_current_user),
    conversations: ConversationRepository = Depends(get_conversation_repo),
):
    return await conversations.list_for_user(user.id)


@router.post("", response_model=ConversationOut)
async def create_conversation(
    user: User = Depends(get_current_user),
    conversations: ConversationRepository = Depends(get_conversation_repo),
):
    return await conversations.create(user.id)


@router.delete("/{conv_id}", status_code=204)
async def delete_conversation(
    conv_id: uuid.UUID,
    user: User = Depends(get_current_user),
    conversations: ConversationRepository = Depends(get_conversation_repo),
):
    conv = await conversations.get_for_user(conv_id, user.id)
    if not conv:
        raise HTTPException(404, "Conversation not found")
    await conversations.delete(conv)


@router.get("/{conv_id}/messages", response_model=list[MessageOut])
async def list_messages(
    conv_id: uuid.UUID,
    user: User = Depends(get_current_user),
    conversations: ConversationRepository = Depends(get_conversation_repo),
    messages: MessageRepository = Depends(get_message_repo),
):
    if not await conversations.get_for_user(conv_id, user.id):
        raise HTTPException(404, "Conversation not found")
    return await messages.list_for_conversation(conv_id)


@router.post("/{conv_id}/messages")
async def send_message(
    conv_id: uuid.UUID,
    body: SendMessage,
    user: User = Depends(get_current_user),
    chat: ChatService = Depends(get_chat_service),
):
    turn = await chat.start_turn(user, conv_id, body.content)  # NotFoundError -> 404 (see main.py)
    return StreamingResponse(chat.stream(turn), media_type="text/event-stream")
