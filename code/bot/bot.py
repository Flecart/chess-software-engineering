"""
Requirements of the bot:

1. A single channel should have at most one game playing at a time (in mob playing)
2. A game should have at least 2 players if it's not a solo game.
3. Only the two designated persons should be able to play (people that started and the other that joined the game
4. If it's a bot game, there is only one player against the bot.

"""

import telebot
import telebot.types as types

import os
from dotenv import load_dotenv
load_dotenv()

bot = telebot.TeleBot(os.getenv("TELEGRAM_TOKEN"))

@bot.message_handler(commands=['hello'])
def handle_hello(message: types.Message):
    print(message)
    bot.reply_to(message, "Hello!")

@bot.message_handler(commands=['start'])
def handle_start(message: types.Message):
    """This function starts a game against a bot

    TODO: add another parameter to specify who starts as what
    
    """
    bot.reply_to(message, "Welcome to the game!")

@bot.message_handler(commands=['join'])
def handle_join(message: types.Message):
    """This function joins a game

    TODO: decide the design of this function
    Another options could be to have a /join <game_id>
    Or just a button to join the game, and should be in a group chat.
    Or the creator of the game should share the game id.
    """
    bot.reply_to(message, "You joined the game!")

@bot.message_handler(commands=['move'])
def handle_move(message: types.Message):
    """This function makes a move in the game
    """

    # TODO: handle move, and the game state, should make request to the backend.
    pass

def start():
    bot.polling()

if __name__ == "__main__":
    start()
