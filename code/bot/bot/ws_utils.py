import websocket
import asyncio
import json
from typing import TypedDict, Literal

from bot.config import ws_url, api_base_url


async def sendWSMessage(url: str, msg: str):
    ws = websocket.WebSocket()
    ws.connect(url)
    ws.send(msg)
    ws.close()


async def receiveWSMessage(url: str):
    ws = websocket.WebSocket()
    ws.connect(url)
    msg = ws.recv()
    ws.close()
    return msg


def sendReceiveMessage(url: str, message: str):
    response_message = None

    def onOpen(ws):
        print("Connessione aperta")
        ws.send(message)

    def onMessage(_, message):
        nonlocal response_message
        response_message = message

    def onClose(_):
        print("Connessione chiusa")

    # Inizializza la connessione WebSocket
    ws = websocket.WebSocketApp(
        url, on_open=onOpen, on_message=onMessage, on_close=onClose
    )
    # Avvia la connessione WebSocket in modo asincrono
    ws.run_forever()
    return response_message


def getWsUrl(gameId: str, token: str) -> str:
    return f"{ws_url}/api/v1/game/{gameId}/ws/?token={token}"


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


class WebSocketWrapper:
    def __init__(self, game_id: str, token: str):
        self.game_id = game_id
        self.token = token
        self.ws = None
        self.url = f"{ws_url}{api_base_url}/game/{self.game_id}/ws?token={self.token}"

    def connect(self):
        self.ws = websocket.WebSocket()
        self.ws.connect(self.get_ws_url())

    def get_ws_url(self) -> str:
        return self.url

    def close(self):
        if self.ws:
            self.ws.close()

    def send(self, msg: Message):
        self.ws.send(json.dumps(msg))

    async def recv(self) -> GameStatus | WaitingStatus:
        result = await asyncio.get_event_loop().run_in_executor(None, self.ws.recv)
        return json.loads(result)
