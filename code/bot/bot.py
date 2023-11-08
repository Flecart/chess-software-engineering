"""
Requirements of the bot:

1. A single channel should have at most one game playing at a time (in mob playing)
2. A game should have at least 2 players if it's not a solo game.
3. Only the two designated persons should be able to play (people that started and the other that joined the game
4. If it's a bot game, there is only one player against the bot.

"""

from api_utils import create_game_api, get_user_status, add_bot,put_move
from display_board import custom_fen_to_svg
from src.user_mapper import UserMapper
from src.game_mapper import GameMapper
import telebot
import telebot.types as types
import requests
import time
import logging
import os

from config import backend,API_TOKEN,DEBUG

logger = telebot.logger

if DEBUG:
    telebot.logger.setLevel(logging.DEBUG)

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def handle_start(message: types.Message):
    bot.send_message(message.chat.id, "Welcome to the game! \n\
        I'm a bot that let's you play Dark chess with your friends! \n\
        Using the current version you will have a text version of the game, \n\
        Run /legend to see the legend of the game. \n\
        Run /rules to see the rules of dark chess game. \n\
        Run /register to register to the game. \n\
        Run /createGameAgainstBot to create a new game and start playing!")
    
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
    bot.send_message(message.chat.id, legend_text)

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
    bot.send_message(message.chat.id, rules_text)


@bot.message_handler(commands=['createGame'])
def create_game(message:types.Message):

    game_id =  create_game_api(message) 
    if game_id is None:
        bot.reply_to(message, "You are already in a game!")
        return

    bot.send_message(message.chat.id,'Invite id is: '+game_id)
    pass


@bot.message_handler(commands=['createGameAgainstBot'])
def create_bot(message:types.Message):
    game_id =  create_game_api(message) 
    if game_id is None:
        bot.reply_to(message, "You are already in a game!")
        return

    add_bot(game_id)

    
    bot.send_message(message.chat.id,'Make a move')
    bot.register_next_step_handler(message,move)


@bot.message_handler(commands=['join'])
def handle_join(message: types.Message):
    """This function joins a game

    TODO: decide the design of this function
    Another options could be to have a /join <game_id>
    Or just a button to join the game, and should be in a group chat.
    Or the creator of the game should share the game id.
    """

    userId = UserMapper().get(message.chat.id)
    GameMapper().add(userId, message.text)

    id = requests.get(backend + f"/game/{message.text}/").json()['game_id']
    if id is None:
        bot.reply_to(message, "The game does not exist!")
    else:
        bot.reply_to(message, "You joined the game!")
        bot.register_next_step_handler(message, move)
    

def move(message: types.Message):

    userId = UserMapper().get(message.chat.id)
    gameId = GameMapper().get(userId)
    current_move = message.text

    put_move(gameId, userId, current_move)
    bot.send_message(message.chat.id, f"Move made,Waiting for the adversary to move")

    game_state = ''
    while True:
        json = get_user_status(userId)
        if json['your_turn']:
            game_state = json['game_state']
            break

        time.sleep(100)

    
    bot.send_photo(message.chat.id, custom_fen_to_svg(game_state)) 
    bot.reply_to(message, '```\n'+game_state+"```", parse_mode="Markdown")

    #TODO adding wrong move handling, finish handling and exit
    bot.send_message(message.chat.id, "Make a move!")
    bot.register_next_step_handler(message, move)


def start():
    bot.polling()

if __name__ == "__main__":
    start()
