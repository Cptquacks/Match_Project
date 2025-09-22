import json, telebot

from user_DB import get_DB, check_ban, read_user, update_user, delete_user

from telebot.types import Message, CallbackQuery
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot.types import ReplyKeyboardMarkup, ReplyKeyboardRemove

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

def get_forms() -> int:
    user_DB : dict = get_DB()
    
    for key in user_DB.keys():
        if check_ban(key) :
            return key
    
    return 0

def get_admins() -> list[str]:    
    with open(file = 'Data/admin_DB.json', mode = 'r', encoding = 'UTF-8') as JSON_Get:
        try :
            admin_DB : list[str] = json.load(JSON_Get)['admins']
            return admin_DB
        
        except KeyError:
            pass
        except IndexError:
            pass
    
    return []

def get_GMessage(message : Message) -> None:
    get_MSG : Message = bot.send_message(chat_id = message.chat.id, text = 'SENDGMSSAGE')
    bot.register_next_step_handler(get_MSG, send_GMessage)


def send_GMessage(message : Message) -> None:
    for key in get_DB().keys():
        bot.send_message(chat_id = int(key), text = f'Mensaje de los administradores: {message.text}')    

def send_forms(message : Message, user_ID : int) -> None:
    user_Form : dict = read_user(user_ID)
    new_KMarkup : ReplyKeyboardMarkup = ReplyKeyboardMarkup(True, True, row_width = 2)
    new_KMarkup.row('Aprobar', 'Rechazar')

    if user_Form['Photo'] != None:
        get_MSG = bot.send_photo(
            chat_id = message.chat.id,
            photo = user_Form['Photo']
        )
    
    get_MSG = bot.send_message(
        chat_id = message.chat.id,
        text = f"Nombre: {user_Form['Name']}\n" f"Edad: {user_Form['Age']}\n" f"Informacion: {user_Form['Info']}",
        reply_markup = new_KMarkup
    )
    
    bot.register_next_step_handler(get_MSG, check_form)

def check_form(message : Message) -> None:
    bot.send_message(chat_id = message.chat.id, text = 'Enviando respuesta', reply_markup = ReplyKeyboardRemove())

    if message.text != 'Aprobar':
        bot.send_message(chat_id = get_forms(), text = 'Su solicitud fue rechazada y su perfil eliminado')
        delete_user(get_forms())
        send_forms(message, get_forms()) if get_forms() != 0 else get_forms()
        return
    
    user_Form : dict = read_user(get_forms())
    user_Form.pop('Baned')

    bot.send_message(chat_id = get_forms(), text = 'Su solicitud fue aprobada y su perfil autorizado')
    update_user(get_forms(), user_Form)
    send_forms(message, get_forms()) if get_forms() != 0 else get_forms()

def handle_feedback(message : Message) -> None:
    for admin in get_admins():
        bot.send_message(chat_id = int(admin), text = f'Mensaje de usuario {read_user(message.chat.id)['Name']}:\n**>>{message.text}', parse_mode = 'MarkdownV2')