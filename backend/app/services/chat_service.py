import json
import uuid
from collections.abc import AsyncIterator, Callable
from dataclasses import dataclass

import httpx

from app.core import settings
from app.models import User, UserSettings
from app.repositories import ConversationRepository, MessageRepository
from app.llm import OllamaClient


class NotFoundError(Exception):
    pass


@dataclass
class Turn:
    """Everything the streaming phase needs, resolved up front so errors surface before the response starts."""

    conversation_id: uuid.UUID
    model: str
    temperature: float
    messages: list[dict]
    set_title_to: str | None


def _sse(payload: dict | str) -> str:
    return f"data: {payload if isinstance(payload, str) else json.dumps(payload)}\n\n"


class ChatService:
    def __init__(
        self,
        conversations: ConversationRepository,
        messages: MessageRepository,
        llm: OllamaClient,
        repo_factory: Callable,  # opens a fresh session + repos for post-stream persistence
    ):
        self.conversations = conversations
        self.messages = messages
        self.llm = llm
        self.repo_factory = repo_factory

    async def start_turn(self, user: User, conv_id: uuid.UUID, content: str) -> Turn:
        conv = await self.conversations.get_for_user(conv_id, user.id)
        if not conv:
            raise NotFoundError("Conversation not found")
        cfg = user.settings or UserSettings()

        await self.messages.create(conv.id, "user", content)
        history = await self.messages.recent(conv.id, settings.history_limit)

        # Prompt assembly. Conversation summary + long-term memories get injected here.
        prompt = [{"role": "system", "content": cfg.system_prompt}]
        prompt += [{"role": m.role, "content": m.content} for m in history]

        return Turn(
            conversation_id=conv.id,
            model=cfg.model,
            temperature=cfg.temperature,
            messages=prompt,
            set_title_to=content[:50] if len(history) == 1 else None,
        )

    async def stream(self, turn: Turn) -> AsyncIterator[str]:
        parts: list[str] = []
        try:
            async for token in self.llm.stream_chat(turn.model, turn.messages, turn.temperature):
                parts.append(token)
                yield _sse({"token": token})
        except (httpx.HTTPError, json.JSONDecodeError) as e:
            yield _sse({"error": f"LLM backend error: {e}"})
        finally:
            # Also runs when the client disconnects ("stop generating"): keep the partial reply.
            full = "".join(parts)
            if full:
                async with self.repo_factory() as (conversations, messages):
                    await messages.create(turn.conversation_id, "assistant", full)
                    if turn.set_title_to:
                        await conversations.set_title(turn.conversation_id, turn.set_title_to)
        yield _sse("[DONE]")
