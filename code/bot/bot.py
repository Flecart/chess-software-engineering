import random
import telebot
from telebot import async_telebot as as_telebot
import telebot.types as types
import logging
import asyncio

from game_loop import game_loop
from config import API_TOKEN,DEBUG,TIME_TO_VOTE_IN_SECONDS

# logger = telebot.logger

if DEBUG:
    telebot.logger.setLevel(logging.DEBUG)

if API_TOKEN:
    bot = as_telebot.AsyncTeleBot(API_TOKEN)
else:
    exit(-1)

@bot.message_handler(commands=['newGame'])
async def startNewGame(message : types.Message): # 
    
    time_to_choose = TIME_TO_VOTE_IN_SECONDS

    args = message.text.split(" ")
    if len(args) > 1:
        try:
            time_to_choose = int(args[1])
        except:
            pass





    # initialisation
    
    await game_loop(time_to_choose,message.chat.id,bot)


@bot.message_handler(commands=['leave','surrender','end'])
async def surrender(message : types.Message):
    await bot.reply_to(message, 'not implemented')

@bot.message_handler(commands=['vote'])
async def vote(message : types.Message):
    args = ""
    _, args = message.text.split(" ",1)

    await bot.reply_to(message, f'not implemented, but you voted {args}')

def start():
    asyncio.run(bot.polling())

if __name__ == "__main__":
    start()
