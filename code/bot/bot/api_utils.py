import requests

from bot.config import backend_url, api_base_url

from bot.src.game_mapper import GameMapper
from bot.src.user_mapper import UserMapper
from bot.ws_utils import WebSocketWrapper

def get_user(chat_id: int):
    token = UserMapper().get(chat_id)
    if token is not None:
        return token
    token = requests.post(backend_url + f"{api_base_url}/user/guest").json()
    UserMapper().add(chat_id, token)
    return token


def create_game(chat_id: int, color: str = "white") -> tuple[str,int]:
    token = get_user(chat_id)
    current_game = GameMapper().get(chat_id)
    if current_game is not None:
        return token, current_game
    body = {"against_bot": True, "type": "dark_chess", "time": 0}
    game = requests.post(
        backend_url + f"{api_base_url}/game",
        json=body,
        headers={"Authorization": token},
    ).json()
    requests.put(
        backend_url + f"{api_base_url}/game/{game}/join/{color}",
        headers={"Authorization": token},
    )
    GameMapper().add(chat_id, game)
    return token, game


def delete_game(chat_id: int):
    current_game = GameMapper().get(chat_id)
    if current_game is None:
        return
    GameMapper().remove(chat_id)


async def make_move(ws: WebSocketWrapper, move: str):
    ws.send({"kind": "move", "data": move})
    response = await ws.recv()
    if "waiting" in response:
        raise ValueError("Unexpected waiting status")
    return response


async def get_possible_moves(ws: WebSocketWrapper):
    ws.send({"kind": "list_move", "data": ""})
    response = await ws.recv()
    if "waiting" in response:
        raise ValueError("Unexpected waiting status")
    return response


async def wait_opponent_move(ws: WebSocketWrapper):
    while True:
        message = await ws.recv()
        if "waiting" not in message:
            return message
