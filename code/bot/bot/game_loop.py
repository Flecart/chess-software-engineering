import asyncio
from datetime import datetime, timedelta
from telebot.async_telebot import AsyncTeleBot
from bot.api_utils import create_game, delete_game, get_possible_moves, make_move, wait_opponent_move
from bot.ws_utils import GameStatus, WebSocketWrapper
from bot.src.ballot_box_collection import BallotBoxCollection


async def game_loop(time: int, chatid: int, bot: AsyncTeleBot):
    """
    time := tempo per votare una mossa
    chatid := id chat dov'è stata avviata la partita
    bot := l'istanza del bot in esecuzione
    """
    token, game_id = create_game(chatid)
    ws = WebSocketWrapper(game_id, token)
    possible_moves = []
    max_voted = ''
    gamestatus = await ws.connect()

    while True:
        # stampa mossa avversaria -> avvia voto -> salva & invia voto -> 

        # get bot move

        await bot.send_message(chatid, gamestatus['view'] )

        if gamestatus['ended']:
            await bot.send_message(chatid,'partita finita!!!')
            ws.close()
            break

        possible_moves = await get_possible_moves(ws)
        ws.close()

        # start time to vote
        current_time = datetime.now()
        end_vote_time = current_time + timedelta(seconds=time)

        await bot.send_message(
            chatid,
            f'le mosse possibili sono { ", ".join(possible_moves)}'
        )
        await bot.send_message(
            chatid,
            f'vota la mossa! Hai tempo fino alle {end_vote_time.strftime("%H:%M:%S")}',
        )

        await asyncio.sleep(time)

        # chiudere votazione e inviare la mossa scelta


        max_voted = BallotBoxCollection().mostVoted(chatid)
        BallotBoxCollection().reset_box(chatid)

        await ws.connect()

        gamestatus = await make_move(ws,max_voted)


        await bot.send_message(
            chatid,
            f'ecco la board aggiornata {gamestatus["view"] }'
        )

        gamestatus = await wait_opponent_move(ws)


    delete_game(chatid)

