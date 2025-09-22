import json, telebot

from user_DB import read_user, update_user, delete_user

from telebot.types import Message, CallbackQuery
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot.types import ReplyKeyboardMarkup, ReplyKeyboardRemove


bot : telebot.TeleBot

def show_profile(chat_ID : int, user_ID : int) -> None:
    if read_user(user_ID)['Photo'] != None:
        bot.send_photo(
            chat_id = chat_ID,
            photo = read_user(user_ID)['Photo']
        )

    bot.send_message(
        chat_id = chat_ID,
        text = (
            f'Nombre:{read_user(user_ID)['Name']}\n'
            f'Edad:{read_user(user_ID)['Age']}\n'
            f'Informacion:\n{read_user(user_ID)['Info']}'
        )
    )
    

def show_settings(message : Message) -> None:
    user_Form : dict = read_user(message.chat.id)

    n_KMarkup : InlineKeyboardMarkup = InlineKeyboardMarkup(row_width = 3)
    n_KMarkup.row(
        InlineKeyboardButton('Nombre', callback_data = 'settings_Name'),
        InlineKeyboardButton('Edad', callback_data = 'settings_Age'),
        InlineKeyboardButton('Foto', callback_data = 'settings_Photo')
    )
    n_KMarkup.row(
        InlineKeyboardButton('Descripcion', callback_data = 'settings_Info'),
        InlineKeyboardButton('Genero', callback_data = 'settings_Gender'),
        InlineKeyboardButton('Preferencia', callback_data = 'settings_Preference')
    )
    n_KMarkup.row(
        InlineKeyboardButton('Eliminar perfil', callback_data = 'settings_delete'),
        InlineKeyboardButton('Salir', callback_data = 'settings_back')
    )
    
    try:
        if user_Form['Photo'] != None:
            bot.send_photo(
                chat_id = message.chat.id, 
                photo = user_Form['Photo']
            )
    except KeyError:
        pass
    
    bot.send_message(
        chat_id = message.chat.id,
        text = (
            f'Nombre:{user_Form['Name']}\n'
            f'Edad:{user_Form['Age']}\n'
            f'Informacion:\n{user_Form['Info']}\n\n'
            f'Genero:{user_Form['Gender']}\n'
            f'Preferencia:{user_Form['Preference']}'
        ),
        reply_markup = n_KMarkup
    )
    @bot.callback_query_handler(lambda call : call.data.startswith('settings_'))
    def handle_callback(callback_Data : CallbackQuery) -> None:

        callback_Data.data = str(callback_Data.data).split('_')[1]
        user_Form : dict = read_user(callback_Data.message.chat.id)
        
        print(callback_Data.data)

        if callback_Data.data == f'{callback_Data.message.chat.id}':
            bot.send_message(chat_id = callback_Data.message.chat.id, text = 'Su usuario ha sido eliminado')
            delete_user(callback_Data.message.chat.id)

        if user_Form.__contains__(callback_Data.data) and not user_Form.__contains__('Baned'):
            user_Form['Baned'] = True
            update_user(callback_Data.message.chat.id, user_Form)

        if callback_Data.data == 'Gender':
            change_gender(callback_Data.message) #type: ignore

        elif callback_Data.data == 'Preference':
            change_gender(callback_Data.message) #type: ignore

        elif callback_Data.data in ['Photo', 'Name', 'Age', 'Info'] :
            change_key(callback_Data.message, callback_Data.data) #type: ignore
        
        elif callback_Data.data == 'delete':
            new_KMarkup : InlineKeyboardMarkup = InlineKeyboardMarkup(row_width = 2)
            new_KMarkup.row(
                InlineKeyboardButton('Si', callback_data = callback_Data.message.chat.id), #type: ignore
                InlineKeyboardButton('No', callback_data = 'null'), #type: ignore

            )
            bot.send_message(chat_id = callback_Data.message.chat.id, text = 'Esta seguro de realizar esta accion???', reply_markup = new_KMarkup)

        elif callback_Data.data == 'back':
            bot.delete_message(chat_id = callback_Data.message.chat.id, message_id = callback_Data.message.id) #type:ignore


def change_key(message : Message, key : str) -> None:
    new_KMarkup : ReplyKeyboardMarkup = ReplyKeyboardMarkup(True)
    new_KMarkup.add('Cancelar')

    get_MSG : Message = bot.send_message(chat_id = message.chat.id, text = 'Envie los datos nuevos a continuacion', reply_markup = new_KMarkup)
    bot.register_next_step_handler(get_MSG, set_key, key)

def set_key(message : Message, key : str) -> None:
    user_Form : dict = read_user(message.chat.id)
    bot.send_message(chat_id = message.chat.id, text = 'Espere un momento...')

    if message.text == 'Cancelar' or not user_Form.__contains__(key):
        show_settings(message)
        return

    if key == 'Photo':
        user_Form['Photo'] = message.photo[0].file_id # type:ignore
    
    elif key == 'Age':
        user_Form['Age'] = int(message.text)#type:ignore

    else :
        user_Form[key] = message.text
    
    update_user(message.chat.id, user_Form)
    bot.send_message(chat_id = message.chat.id, text = 'Sus cambios fueron realizados y estan pendientes a aprobacion')
    


def change_gender(message : Message) -> None:
    new_KMarkup : ReplyKeyboardMarkup = ReplyKeyboardMarkup(True, True, row_width = 2)
    new_KMarkup.row('Masculino', 'Femenino')
    new_KMarkup.add('Cancelar')

    get_MSG : Message = bot.send_message(chat_id = message.chat.id, text = "Elija su genero a continuacion", reply_markup = new_KMarkup)
    bot.register_next_step_handler(get_MSG, set_gender)

def set_gender(message : Message) -> None:
    gender_List : list[str] = ['Masculino', 'Femenino']

    if str(message.text).capitalize() == 'Cancelar':
        show_settings(message)
        return
    
    if str(message.text).capitalize() not in gender_List:
        change_gender(message)
        return
    
    user_Form : dict = read_user(message.chat.id)
    user_Form['Gender'] = str(message.text).capitalize()

    update_user(message.chat.id, user_Form)

    bot.send_message(chat_id = message.chat.id, text = 'Informacion actualizada', reply_markup = ReplyKeyboardRemove())
    show_settings(message)


def change_preference(message : Message) -> None:
    new_KMarkup : ReplyKeyboardMarkup = ReplyKeyboardMarkup(True, True, row_width = 2)
    new_KMarkup.row('Masculino', 'Femenino', 'Ambos')
    new_KMarkup.add('Cancelar')

    get_MSG : Message = bot.send_message(chat_id = message.chat.id, text = "Elija el genero de su pareja ideal a continuacion", reply_markup = new_KMarkup)
    bot.register_next_step_handler(get_MSG, set_preference)

def set_preference(message : Message) -> None:
    gender_List : list[str] = ['Masculino', 'Femenino', 'Ambos']

    if str(message.text).capitalize() == 'Cancelar':
        show_settings(message)
        return
    
    if str(message.text).capitalize() not in gender_List:
        change_gender(message)
        return
    
    user_Form : dict = read_user(message.chat.id)
    user_Form['Preference'] = str(message.text).capitalize()

    update_user(message.chat.id, user_Form)

    bot.send_message(chat_id = message.chat.id, text = 'Informacion actualizada', reply_markup = ReplyKeyboardRemove())
    show_settings(message)