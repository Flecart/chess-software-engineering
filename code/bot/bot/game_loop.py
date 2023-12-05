import asyncio
from datetime import datetime, timedelta
from telebot.async_telebot import AsyncTeleBot
from bot.api_utils import create_game, delete_game
from bot.ws_utils import WebSocketWrapper


async def game_loop(time: int, chatid: int, bot: AsyncTeleBot):
    """
    time := tempo per votare una mossa
    chatid := id chat dov'è stata avviata la partita
    bot := l'istanza del bot in esecuzione
    """
    token, game_id = create_game(chatid)
    ws = WebSocketWrapper(game_id, token)

    while True:  # TODO chiudere il loop quando finisce la partita

        current_time = datetime.now()
        end_vote_time = current_time + timedelta(seconds=time)

        await bot.send_message(
            chatid,
            f'vota la mossa! Hai tempo fino alle {end_vote_time.strftime("%H:%M:%S")}',
        )

        # websocket interaction
        ws.connect()
        opening_message = await ws.recv()
        print(opening_message)
        ws.close()

        # stampare broard

        await asyncio.sleep(time)

        # chiudere votazione e inviare la mossa scelta
    delete_game(chatid)
