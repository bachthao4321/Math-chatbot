from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class ChatInput(BaseModel):
    user_input: str
    session_id: str




