import json, telebot

from user_DB import read_user, update_user, delete_user

from telebot.types import Message, CallbackQuery
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot.types import ReplyKeyboardMarkup, ReplyKeyboardRemove

bot : telebot.TeleBot

def show_settings(message : Message) -> None:
    user_Form : dict = read_user(message.chat.id)

    n_KMarkup : InlineKeyboardMarkup = InlineKeyboardMarkup(row_width = 3)
    n_KMarkup.row(
        InlineKeyboardButton('Nombre', callback_data = 'Name'),
        InlineKeyboardButton('Edad', callback_data = 'Age'),
        InlineKeyboardButton('Foto', callback_data = 'Photo')
    )
    n_KMarkup.row(
        InlineKeyboardButton('Descripcion', callback_data = 'Info'),
        InlineKeyboardButton('Genero', callback_data = 'Gender'),
        InlineKeyboardButton('Preferencia', callback_data = 'Preference')
    )
    n_KMarkup.row(
        InlineKeyboardButton('Eliminar perfil', callback_data = 'delete'),
        InlineKeyboardButton('Salir', callback_data = 'back')
    )

    if user_Form['Photo'] != None:
        bot.send_photo(
            chat_id = message.chat.id, 
            photo = user_Form['Photo']
        )
    
    bot.send_message(
        chat_id = message.chat.id,
        text = "Opciones de edicion",
        reply_markup = n_KMarkup
    )