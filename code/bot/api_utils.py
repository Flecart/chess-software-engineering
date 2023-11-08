import requests
import telebot.types as types
from dotenv import load_dotenv

from src.user_mapper import UserMapper
from src.game_mapper import GameMapper
from config import backend



def get_user(idChat):
    userId = UserMapper().get(idChat)
    if userId is not None:
        return userId
    json = requests.get(backend + "/user/new").json()
    userId = json['id']

    UserMapper().add(idChat, userId)
    return userId


def create_game_api(message: types.Message) ->str|None:
    """create a game and player if the chat id is not in a game"""
    
    userId = get_user(message.chat.id)
    
    current_game = GameMapper().get(userId)
    if current_game is not None:
        return None
    id = requests.get(backend+'/game/create').json()['game_id']

    GameMapper().add(userId,id)

    requests.get(backend+f'/game/join/{id}/{userId}/white')

    return id

def leave_game(message: types.Message) -> str|None:
    """This function leaves a game
    TODO: should handle the backend side too
    """
    userId = get_user(message.chat.id)
    user = GameMapper().remove(userId)
    return user

add_bot = lambda id: requests.get(backend+f'/game/add-bot/{id}/')

get_user_status = lambda userId: requests.get(backend + f"/user/status/{userId}").json()

put_move = lambda gameId, userId, move: requests.get(backend + f"/game/move/{gameId}/{userId}/{move}").json()