import json, telebot

from user_DB import get_DB, check_ban, read_user, update_user, delete_user

from telebot.types import Message, CallbackQuery
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

bot : telebot.TeleBot

def check_admin(user_ID : int) -> bool:
    with open(file = 'Data/admin_DB.json', mode = 'r', encoding = 'UTF-8') as JSON_Get:
        try :
            admin_DB : list = json.load(JSON_Get)['admins']
            return admin_DB.__contains__(f'{user_ID}')
        except KeyError:
            pass
        except IndexError:
            pass

    return False

def get_forms(message : Message) -> None:
    user_DB : dict = get_DB()
    
    for key in user_DB.keys():
        if check_ban(key) :
            send_forms(message, key)

def send_forms(message : Message, user_ID : int) -> None:
    user_Form : dict = read_user(user_ID)
    new_KMarkup : InlineKeyboardMarkup = InlineKeyboardMarkup(row_width = 2)
    new_KMarkup.row(
        InlineKeyboardButton('Aprobar', callback_data = f'{user_ID}'),
        InlineKeyboardButton('No aprobar', callback_data = 'not')
    )

    if user_Form['Photo'] != None:
        bot.send_photo(
            chat_id = message.chat.id,
            photo = user_Form['Photo'],
            caption = f"Nombre: {user_Form['Name']}\n" f"Edad: {user_Form['Age']}\n" f"Informacion: {user_Form['Info']}",
            reply_markup = new_KMarkup
        )
    
    elif user_Form['Photo'] == None:
        bot.send_message(
            chat_id = message.chat.id,
            text = f"Nombre: {user_Form['Name']}\n" f"Edad: {user_Form['Age']}\n" f"Informacion: {user_Form['Info']}",
            reply_markup = new_KMarkup
        )
    
    @bot.callback_query_handler()
    def handle_permission(callback_Data : CallbackQuery) -> None:
        try :
            user_Form.pop('Baned')

        except KeyError:
            return

        if callback_Data.data == user_ID:
            print('request Accepted')
            update_user(user_ID, user_Form)
            bot.delete_message(chat_id = callback_Data.message.chat.id, message_id = callback_Data.message.id)# type: ignore
            bot.send_message(chat_id = user_ID, text = 'Su usuario a sido aprobado!')
        
        else :
            print('request Denied')
            delete_user(user_ID)
            bot.delete_message(chat_id = callback_Data.message.chat.id, message_id = callback_Data.message.id)# type: ignore