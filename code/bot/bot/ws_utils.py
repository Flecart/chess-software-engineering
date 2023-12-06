import websocket
import asyncio
import json
from typing import TypedDict, Literal

from bot.config import ws_url, api_base_url


class Message(TypedDict):
    kind: Literal["move", "list_move"]
    data: str


class GameStatus(TypedDict):
    ended: bool
    possible_moves: list[str] | None
    view: str
    move_made: str | None
    turn: str


class WaitingStatus(TypedDict):
    waiting: bool


none_ws_error = TypeError("ws is None, call connect() first")


class WebSocketWrapper:
    def __init__(self, game_id: int, token: str):
        self.game_id = game_id
        self.token = token
        self.ws = None
        self.url = f"{ws_url}{api_base_url}/game/{self.game_id}/ws?token={self.token}"

    async def connect(self) -> GameStatus:
        self.ws = websocket.WebSocket()
        self.ws.connect(self.get_ws_url())

        response = await self.recv()

        if "waiting" in response:
            raise ValueError("Unexpected waiting status")

        return response

    def get_ws_url(self) -> str:
        return self.url

    def close(self):
        if self.ws is None:
            raise none_ws_error
        self.ws.close()

    def send(self, msg: Message):
        if self.ws is None:
            raise none_ws_error
        self.ws.send(json.dumps(msg))

    async def recv(self) -> GameStatus | WaitingStatus:
        if self.ws is None:
            raise none_ws_error
        result = await asyncio.get_event_loop().run_in_executor(None, self.ws.recv)
        return json.loads(result)
