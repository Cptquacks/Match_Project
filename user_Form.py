import json, telebot
from user_DB import STD_UserForm
from user_DB import create_user

from telebot.types import Message
from telebot.types import ReplyKeyboardMarkup
from telebot.types import ReplyKeyboardRemove

new_user : dict = STD_UserForm
bot : telebot.TeleBot

def set_bot(bot_Object : telebot.TeleBot) -> None:
    if bot_Object == None :
        return
    
    bot = bot_Object


def get_name(message : Message) -> None:
    new_KMarkup : ReplyKeyboardMarkup = ReplyKeyboardMarkup(True, True, None, 1)
    new_KMarkup.add(message.chat.first_name)
    
    get_MSG = bot.send_message(chat_id = message.chat.id, text = f'Introduzca su nombre debajo o utilice su nombre de usuario', reply_markup = new_KMarkup)
    bot.register_next_step_handler(get_MSG, set_name)

def set_name(message : Message) -> None:
    tar_MSG = bot.send_message(chat_id = message.chat.id, text = f'Espere un momento...', reply_markup = ReplyKeyboardRemove())
    new_user['Name'] = message.text if str(message.text).__len__() > 0 else None #Ternary operator used
    bot.delete_message(chat_id = message.chat.id, message_id = tar_MSG.id)

    get_age(message)

    

def get_age(message : Message) -> None:
    new_KMarkup : ReplyKeyboardMarkup = ReplyKeyboardMarkup(True, True, None, 1)
    new_KMarkup.add('Prefiero no decirlo')

    get_MSG = bot.send_message(chat_id = message.chat.id, text = f'Introduzca su edad', reply_markup = new_KMarkup)
    bot.register_next_step_handler(get_MSG, set_age)

def set_age(message : Message) -> None:
    
    tar_MSG = bot.send_message(chat_id = message.chat.id, text = f'Espere un momento...', reply_markup = ReplyKeyboardRemove())
    new_user['Age'] = message.text if str(message.text).isnumeric() else None #Ternary operator used
    bot.delete_message(chat_id = message.chat.id, message_id = tar_MSG.id)