import telebot
from telebot import async_telebot as as_telebot
import telebot.types as types
import logging
import asyncio

from bot.game_loop import game_loop
from bot.config import API_TOKEN, DEBUG, TIME_TO_VOTE_IN_SECONDS
from bot.src.ballot_box_collection import BallotBoxCollection
from bot.utils import get_user_and_chat_from_message
from bot.src.valid_moves_mapper import ValidMovesMapper
from bot.texts import help_text,rules_text
# logger = telebot.logger

if DEBUG:
    telebot.logger.setLevel(logging.DEBUG)

if API_TOKEN:
    bot = as_telebot.AsyncTeleBot(API_TOKEN)
else:
    exit(-1)


@bot.message_handler(commands=["newGame"])
async def startNewGame(message: types.Message):
    time_to_choose = TIME_TO_VOTE_IN_SECONDS
    args = [10*60] # hardcoded just in case .env explode

    if message.text is not None:
        args = message.text.split(" ")
    if len(args) > 1:
        try:
            time_to_choose = int(args[1])
        except:
            pass

    # initialisation

    await game_loop(time_to_choose, message.chat.id, bot)




@bot.message_handler(commands=["vote"])
async def vote(message: types.Message):
    args = ""
    if message.text is not None:
        _, args = message.text.split(" ", 1)
    else:
        pass
    (chad_id, user_id) = get_user_and_chat_from_message(message)
    valid_moves = ValidMovesMapper().get(chad_id)
    if valid_moves is not None:
        if args not in valid_moves:
            await bot.reply_to(message, "Mossa invalida")
            return
    try:  # demo
        BallotBoxCollection().add_vote(chad_id, user_id, vote=args)
    except Exception as e:
        await bot.reply_to(message, str(e))
    else:
        await bot.reply_to(
            message,
            f"per il momento la mossa più votata è {BallotBoxCollection().mostVoted(chad_id)}",
        )

@bot.message_handler(commands=["help"])
async def help(message: types.Message):
    await bot.reply_to(message, help_text)

@bot.message_handler(commands=["rules"])
async def rules(message: types.Message):
    await bot.reply_to(message, rules_text)

@bot.message_handler(commands=["leave", "surrender", "end"])
async def vote_for_leave_game(message: types.Message):
    (chat_id,user_id) = get_user_and_chat_from_message(message)

    BallotBoxCollection().add_vote(chat_id,user_id,"leave")

    await bot.reply_to(message,
                       "hai votato per chiudere la partita")

def start():
    print("Ready")
    asyncio.run(bot.polling())


if __name__ == "__main__":
    start()
