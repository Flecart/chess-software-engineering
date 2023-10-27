import telebot
import os
from dotenv import load_dotenv
load_dotenv()

bot = telebot.TeleBot("2042098134:AAHeiol_7Ux8ArrMaBtQUgDMfFDN5mGzp_o")

@bot.message_handler(commands=['hello'])
def handle_hello(message):
    bot.reply_to(message, "Hello!")

bot.polling()
