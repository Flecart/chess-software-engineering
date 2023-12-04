import requests

from bot.config import backend as backend_url

from bot.src.game_mapper import GameMapper
from bot.src.user_mapper import UserMapper


def get_user(chatId: str):
    token = UserMapper().get(chatId)
    if token is not None:
        return token
    token = requests.post(backend_url + "/user/guest").json()
    UserMapper().add(chatId, token)
    return token


def create_game(chatId: str):
    token = get_user(chatId)
    current_game = GameMapper().get(chatId)
    if current_game is not None:
        return token, current_game
    body = {"against_bot": True, "type": "dark_chess"}
    game = requests.post(
        backend_url + "/game", json=body, headers={"Authorization": token}
    ).json()
    GameMapper().add(chatId, game)
    requests.post(
        backend_url + "/game/" + game + "/join", headers={"Authorization": token}
    )
    return token, game
