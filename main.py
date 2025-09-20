import os, telebot
import user_DB, user_Form, admin_Utils, profile_Utils

from telebot.types import Message
from telebot.types import BotCommand

from telebot.types import ReplyKeyboardMarkup
from telebot.types import ReplyKeyboardRemove
from telebot.types import KeyboardButton




bot : telebot.TeleBot = telebot.TeleBot('6402990173:AAFty3Z7TuSzuDdjkmoModOn3J8kMAhFM-I')
STD_F : str = 'MarkdownV2'
HTM_F : str = 'HTML'



@bot.message_handler(commands = ['start'], chat_types = ['private'])
def handle_start(message : Message) -> None:
    if not user_DB.check_user(message.chat.id) :
        bot.send_message(chat_id = message.chat.id, text = f'Hola {message.chat.first_name} *bienvenido a UCItas*', parse_mode = STD_F)
        user_Form.bot = bot
        user_Form.get_name(message)
        
        return
    
@bot.message_handler(commands = ['settings'], chat_types = ['private'])
def handle_settings(message : Message) -> None:
    if not user_DB.check_user(message.chat.id) and user_DB.check_ban(message.chat.id) :
        return
    
    profile_Utils.bot = bot
    profile_Utils.show_settings(message)


#Admin commands
@bot.message_handler(commands = ['get_chat_id'], chat_types = ['private'])
def handle_GCIC(message : Message) -> None:
    bot.send_message(chat_id = message.chat.id, text = f'`{message.chat.id}`', parse_mode = STD_F)

@bot.message_handler(commands = ['get_user_forms'], chat_types = ['private'])
def handle_GUFC(message : Message) -> None:
    if not admin_Utils.check_admin(message.chat.id) :
        return
    
    admin_Utils.bot = bot
    admin_Utils.send_forms(message, admin_Utils.get_forms())




bot.set_my_commands([
    BotCommand('start', 'Pone en marcha el bot'),
    BotCommand('profile', 'Accede a la informacion de perfil'),
    BotCommand('settings', 'Abre las opciones del perfil')
])

os.system('clear')
print("DEBUG START")
bot.infinity_polling()
print("DEBUG END")