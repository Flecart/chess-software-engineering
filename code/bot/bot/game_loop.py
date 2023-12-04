import asyncio
from datetime import datetime, timedelta
from telebot.async_telebot import AsyncTeleBot


async def game_loop(time : int, chatid: int, bot : AsyncTeleBot):
    """
        time := tempo per votare una mossa
        chatid := id chat dov'è stata avviata la partita
        bot := l'istanza del bot in esecuzione
    """
    while True: # TODO chiudere il loop quando finisce la partita
        
        # Get the current time
        current_time = datetime.now()

        # Add five minutes
        end_vote_time = current_time + timedelta(seconds=time)

        await bot.send_message(chatid, f'vota la mossa! Hai tempo fino alle {end_vote_time.strftime("%H:%M:%S")}')

        # stampare broard

        await asyncio.sleep(time)

        # chiudere votazione e inviare la mossa scelta
    
