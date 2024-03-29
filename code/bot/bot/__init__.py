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
from bot.src.game_mapper import GameMapper
from bot.texts import help_text, rules_text


if DEBUG:
    telebot.logger.setLevel(logging.DEBUG)

if API_TOKEN:
    bot = as_telebot.AsyncTeleBot(API_TOKEN)
else:
    exit(-1)


@bot.message_handler(commands=["newgame"])
async def start_new_game(message: types.Message):
    if GameMapper().get(message.chat.id) is not None:
        await bot.reply_to(
            message, "C'è un'altra partita in corso, usa /leave se vuoi votare la resa"
        )
        return
    time_to_choose = TIME_TO_VOTE_IN_SECONDS
    args = [10 * 60]  # hardcoded just in case .env explode

    if message.text is not None:
        args = message.text.split(" ")
    if len(args) > 1:
        try:
            time_to_choose = int(args[1])
        except Exception:
            pass

    # initialisation

    await game_loop(time_to_choose, message.chat.id, bot)


@bot.message_handler(commands=["vote"])
async def vote(message: types.Message):
    args = ""
    if message.text is not None:
        _, args = message.text.split(" ", 1)
    else:
        return

    (chad_id, user_id) = get_user_and_chat_from_message(message)
    valid_moves = ValidMovesMapper().get(chad_id)

    if valid_moves is not None and args not in valid_moves:
        await bot.reply_to(message, "Mossa invalida")
        return

    try:
        BallotBoxCollection().add_vote(chad_id, user_id, vote=args)
    except Exception as e:
        await bot.reply_to(message, str(e))
    else:
        most_voted = BallotBoxCollection().mostVoted(chad_id)
        if most_voted is None:
            await bot.reply_to(message, "Nessuna mossa votata")
        else:
            await bot.reply_to(
                message,
                f"Per il momento la mossa più votata è {', '.join(most_voted)}",
            )


@bot.message_handler(commands=["help"])
async def help(message: types.Message):
    await bot.reply_to(message, help_text)


@bot.message_handler(commands=["rules"])
async def rules(message: types.Message):
    await bot.reply_to(message, rules_text)


@bot.message_handler(commands=["leave", "surrender", "end"])
async def vote_for_leave_game(message: types.Message):
    (chat_id, user_id) = get_user_and_chat_from_message(message)

    BallotBoxCollection().add_vote(chat_id, user_id, "leave")

    await bot.reply_to(message, "hai votato per chiudere la partita")


def start():
    print("Ready")
    asyncio.run(bot.polling())


if __name__ == "__main__":
    start()
