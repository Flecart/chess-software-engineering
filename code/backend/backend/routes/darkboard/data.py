from pydantic import BaseModel
import datetime
from typing import Literal
from backend.bot.darkboard_adapter import DarkBoardStates

    
class GameStatusResponse(BaseModel):
    state: DarkBoardStates
    fen: str
    message: list[str]|None
    error_message: str|None = None

