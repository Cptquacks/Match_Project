import os, telebot
import user_DB, user_Form

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
    if not user_DB.check_user(message.chat.id) :
        bot.send_message(chat_id = message.chat.id, text = f'Hola {message.chat.first_name} *bienvenido a UCItas*', parse_mode = STD_F)
        user_Form.bot = bot
        user_Form.get_name(message)
        return




os.system('clear')
print("DEBUG START")
bot.infinity_polling()
print("DEBUG END")