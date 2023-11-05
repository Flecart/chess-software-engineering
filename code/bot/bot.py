"""
Requirements of the bot:

1. A single channel should have at most one game playing at a time (in mob playing)
2. A game should have at least 2 players if it's not a solo game.
3. Only the two designated persons should be able to play (people that started and the other that joined the game
4. If it's a bot game, there is only one player against the bot.

"""

from src.UserMapper import UserMapper
from src.GameMapper import GameMapper
import telebot
import telebot.types as types
import requests
import time

import os
from dotenv import load_dotenv
load_dotenv()

bot = telebot.TeleBot(os.getenv("TELEGRAM_TOKEN"))
backend = os.getenv("BACKEND_URL")

@bot.message_handler(commands=['start'])
def handle_start(message: types.Message):
    bot.send_message(message.from_user.id, "Welcome to the game! \n\
        I'm a bot that let's you play Dark chess with your friends! \n\
        Using the current version you will have a text version of the game, \n\
        Run /legend to see the legend of the game. \n\
        Run /rules to see the rules of dark chess game. \n\
        Run /register to register to the game. \n\
        Run /createGame to create a new game and start playing!")
    
@bot.message_handler(commands=['help'])
def handle_help(message: types.Message):
    handle_start(message)

@bot.message_handler(commands=['legend'])
def handle_legend(message: types.Message):
    legend_text = """
Upper case is white player
Lower case is black player
K is king
Q is queen
R is rook
B is bishop
N is knight
P is pawn
. is empty square
X is not visible square
"""
    bot.send_message(message.from_user.id, legend_text)

@bot.message_handler(commands=['rules'])
def handle_rules(message: types.Message):
    rules_text = """
The rules of dark chess are the same of normal chess, with the following differences:
- There is no check or checkmate. Each player can freely move his/her king to a check position.
- The player who captures the opponent's king, wins the game.

Furthermore this version is information incomplete.
The squares that are visible to the player must follow one of these conditions:
- A player's piece stands on that square.
- The player can move a piece to that square. This means that he/she can see empty squares that he/she can move to, or an opponent's piece that he/she can capture.
- The square is directly in front of one of player's pawns or it is an adjacent forward diagonal from one of player's pawns.
See https://brainking.com/en/GameRules for more information
"""
    bot.send_message(message.from_user.id, rules_text)

@bot.message_handler(commands=['register'])
def handle_register(message: types.Message):
    userId = UserMapper().get(message.from_user.id)
    if userId is not None:
        bot.reply_to(message, "You are already registered!")
        return

    json = requests.get(backend + "/user/new").json()
    userId = json['id']

    UserMapper().add(message.from_user.id, userId)


    bot.reply_to(message, f"Welcome to the game!, your user id is '{userId}'.")
    bot.send_message(message.from_user.id, "Create a new Game")

@bot.message_handler(commands=['createGame'])
def create_bot(message:types.Message):
    id = requests.get(backend+'/game/create').json()['game_id']

    userId = UserMapper().get(message.from_user.id)
    if userId is None:
        bot.reply_to(message, "You are not registered, remember to use /start")
        return

    GameMapper().add(userId,id)

    requests.get(backend+f'/game/join/{id}/{userId}/white')
    requests.get(backend+f'/game/add-bot/{id}/')

    bot.send_message(message.from_user.id,'Make a move')
    bot.register_next_step_handler(message,move)


@bot.message_handler(commands=['join'])
def handle_join(message: types.Message):
    """This function joins a game

    TODO: decide the design of this function
    Another options could be to have a /join <game_id>
    Or just a button to join the game, and should be in a group chat.
    Or the creator of the game should share the game id.
    """

    userId = UserMapper().get(message.from_user.id)
    GameMapper().add(userId, message.text)

    id = requests.get(backend + f"/game/{message.text}/").json()['game_id']
    if id is None:
        bot.reply_to(message, "The game does not exist!")
    else:
        bot.reply_to(message, "You joined the game!")
        bot.register_next_step_handler(message, move)
    

def move(message: types.Message):

    userId = UserMapper().get(message.from_user.id)
    gameId = GameMapper().get(userId)
    current_move = message.text

    requests.get(backend + f"/game/move/{gameId}/{userId}/{current_move}").json()
    bot.send_message(message.from_user.id, f"Move made,Waiting for the adversary to move")

    game_state = ''
    while True:
        json = requests.get(backend + f"/user/status/{userId}").json()

        if json['your_turn']:
            game_state = json['game_state']
            break

        time.sleep(100)

    bot.reply_to(message, '```\n'+game_state+"```", parse_mode="Markdown")

    #TODO adding wrong move handling, finish handling and exit
    bot.send_message(message.from_user.id, "Make a move!")
    bot.register_next_step_handler(message, move)


def start():
    bot.polling()

if __name__ == "__main__":
    start()
