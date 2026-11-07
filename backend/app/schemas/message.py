from pydantic import BaseModel
import uuid

class SendMessage(BaseModel):
    content: str


class MessageOut(BaseModel):
    id: uuid.UUID
    role: str
    content: str

    model_config = {"from_attributes": True}
