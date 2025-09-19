import os, telebot
import user_DB

from telebot.types import Message
from telebot.types import BotCommand

from telebot.types import ReplyKeyboardMarkup
from telebot.types import ReplyKeyboardRemove
from telebot.types import KeyboardButton




bot : telebot.TeleBot = telebot.TeleBot('6402990173:AAFty3Z7TuSzuDdjkmoModOn3J8kMAhFM-I')
STD_F : str = 'MarkdownV2'
HTM_F : str = 'HTML'



@bot.message_handler(commands = ['start'])
def handle_Start(message : Message) -> None:
    bot.send_message(message.chat.id, f'Test')





os.system('clear')
print("DEBUG START")
bot.infinity_polling()
print("DEBUG END")