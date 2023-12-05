import requests

from bot.config import backend_url, api_base_url

from bot.src.game_mapper import GameMapper
from bot.src.user_mapper import UserMapper
from bot.ws_utils import WebSocketWrapper
import json


def get_user(chat_id: str):
    token = UserMapper().get(chat_id)
    if token is not None:
        return token
    token = requests.post(backend_url + f"{api_base_url}/user/guest").json()
    UserMapper().add(chat_id, token)
    return token


def create_game(chat_id: str, color: str = "white"):
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


async def make_move(ws: WebSocketWrapper, move: str):
    json_data = json.dumps({"kind": "move", "data": move})
    ws.send(json_data)
    return await ws.recv()


async def get_possible_moves(ws: WebSocketWrapper):
    json_data = json.dumps({"kind": "list_move", "data": ""})
    ws.send(json_data)
    return await ws.recv()
