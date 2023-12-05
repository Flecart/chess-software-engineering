import asyncio
from datetime import timedelta
import random
from telebot.async_telebot import AsyncTeleBot
from bot.api_utils import (
    create_game,
    delete_game,
    get_possible_moves,
    make_move,
    wait_opponent_move,
)
from bot.utils import pretty_print_time
from bot.ws_utils import WebSocketWrapper
from bot.src.ballot_box_collection import BallotBoxCollection
from bot.display_board import custom_fen_to_svg
from bot.src.valid_moves_mapper import ValidMovesMapper


async def game_loop(time: int, chatid: int, bot: AsyncTeleBot):
    """
    time := tempo per votare una mossa
    chatid := id chat dov'è stata avviata la partita
    bot := l'istanza del bot in esecuzione
    """
    color = "white"
    token, game_id = create_game(chatid, color)
    ws = WebSocketWrapper(game_id, token)
    max_voted = ""
    gamestatus = await ws.connect()

    while True:
        # stampa mossa avversaria -> avvia voto -> salva & invia voto
        await bot.send_photo(chatid, custom_fen_to_svg(gamestatus["view"]))

        if gamestatus["ended"]:
            result_message = (
                "avete vinto!" if gamestatus["turn"] != color else "avete perso!"
            )
            await bot.send_message(chatid, f"partita finita!!! {result_message}")
            ws.close()
            break

        possible_moves = await get_possible_moves(ws)
        ValidMovesMapper().add(chatid, possible_moves)
        ws.close()

        # start time to vote

        remaining_time = timedelta(seconds=time)

        await bot.send_message(
            chatid, f'le mosse possibili sono { ", ".join(possible_moves)}'
        )
        await bot.send_message(
            chatid,
            f"vota la mossa! Hai tempo rimanente: {pretty_print_time(remaining_time)}",
        )

        await asyncio.sleep(time)

        # chiudere votazione e inviare la mossa scelta

        max_voted = BallotBoxCollection().mostVoted(chatid)
        BallotBoxCollection().reset_box(chatid)

        await ws.connect()

        # funny easter egg for the time
        mid_time = round(time / 2)
        remaining_mid_time = timedelta(seconds=mid_time)
        if max_voted is None:
            await bot.send_message(chatid, "Hey! C'è ancora qualcuno?")
            await bot.send_message(chatid, f'Va bhe, sono buono, vi darò ancora tempo, ma solo {pretty_print_time(remaining_mid_time)}')
            await asyncio.sleep(mid_time)
            max_voted = BallotBoxCollection().mostVoted(chatid)
        if max_voted is None:
            await bot.send_message(chatid, "Ehi! Non mi prendete in giro!")
            await bot.send_message(chatid, "Se non votate, vi do una mossa a caso(ricordatevi la legge di Murphy!)")
            await asyncio.sleep(mid_time)
            max_voted = BallotBoxCollection().mostVoted(chatid)
        if max_voted is None:
            await bot.send_message(chatid, "Ok, basta, io me ne vado!")
            await bot.send_message(chatid, "Partita finita.")
            break

        gamestatus = await make_move(ws, random.choice(max_voted))

        await bot.send_photo(chatid, custom_fen_to_svg(gamestatus["view"]))

        # get bot move
        gamestatus = await wait_opponent_move(ws)

    ValidMovesMapper().remove(chatid)
    delete_game(chatid)
