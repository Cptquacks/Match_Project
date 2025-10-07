import json, telebot

from bot import bot
from user_DB import get_DB, check_ban, read_user, update_user, delete_user

from telebot.types import Message, CallbackQuery
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot.apihelper import ApiException

user_DB : dict


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
    for key in user_DB.keys():
        if (user_DB[key].__contains__('Baned')) :
            send_forms(message, int(key))
    
    return

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
    get_MSG : Message = bot.send_message(chat_id = message.chat.id, text = 'Escriba el gmsg')
    bot.register_next_step_handler(get_MSG, send_GMessage)


def send_GMessage(message : Message) -> None:
    for key in user_DB.keys():
        try:
            bot.send_message(chat_id = int(key), text = f'Mensaje de los administradores: \n{message.text}')
        except ApiException:
            continue

def send_forms(message : Message, user_ID : int) -> None:
    user_Form : dict = user_DB[f'{user_ID}']

    new_KMarkup : InlineKeyboardMarkup = InlineKeyboardMarkup(row_width = 2)
    new_KMarkup.row(
        InlineKeyboardButton(text = 'Aprobar', callback_data = f'admin_{user_ID}'),
        InlineKeyboardButton(text = 'Rechazar', callback_data = f'admin_dismiss')
    )
    new_KMarkup.add(
        InlineKeyboardButton(text = 'Eliminar', callback_data = f'admin_{user_ID}_delete')
    )

    if user_Form['Photo'] != None:
        get_MSG : Message = bot.send_photo(
            chat_id = message.chat.id,
            photo = user_Form['Photo'],
            caption = (
                f'Nombre:{user_Form['Name']}\n'
                f'Edad: {user_Form['Age']}\n'
                f'Informacion: {user_Form['Info']}\n'
            ),
            reply_markup = new_KMarkup
        )
    
    elif user_Form['Photo'] == None:
        get_MSG : Message = bot.send_message(
            chat_id = message.chat.id,
            text = (
                f'Nombre:{user_Form['Name']}\n'
                f'Edad: {user_Form['Age']}\n'
                f'Informacion: {user_Form['Info']}\n'
            ),
            reply_markup = new_KMarkup
        )
    
@bot.callback_query_handler(lambda call : str(call.data).startswith('admin_'))
def handle_form(callback_Data : CallbackQuery) -> None:
    user_ID : int = int(str(callback_Data.data).split('_')[1])
    user_Form : dict = read_user(user_ID)
    callback_Data.data = str(callback_Data.data).split('_')[1]
    
    try:
        order : str = str(callback_Data.data).split('_')[2]
    except IndexError:
        order : str = 'blank'
    
    bot.send_message(chat_id = callback_Data.message.chat.id, text = 'Enviando respuesta')

    if callback_Data.data == f'{user_ID}':
        user_Form.pop('Baned')
        update_user(user_ID, user_Form)

        bot.send_message(chat_id = user_ID, text = 'Su perfil ha sido aprobado')
        
    elif callback_Data.data == 'dismiss':
        bot.send_message(chat_id = user_ID, text = 'Su perfil no ha sido aprobado, intente hacer cambios en el')

    elif callback_Data.data == 'delete':
        delete_user(user_ID)
        bot.send_message(chat_id = user_ID, text = 'Su perfil ha sido eliminado')
    
    bot.delete_message(chat_id = callback_Data.message.chat.id, message_id = callback_Data.message.id) #type: ignore

def handle_feedback(message : Message) -> None:
    for admin in get_admins():
        bot.send_message(chat_id = int(admin), text = f'Mensaje de usuario {read_user(message.chat.id)['Name']}:\n**>>{message.text}', parse_mode = 'MarkdownV2')