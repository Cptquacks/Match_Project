import json, telebot, random, profile_Utils

from user_DB import read_user, get_DB, update_user
from admin_Utils import get_admins

from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from telebot.types import CallbackQuery, Message

bot : telebot.TeleBot
debug : bool = False


#Like list methods
def has_LList(message : Message) -> bool:
    user_Form : dict = read_user(message.chat.id)
    if user_Form.__contains__('likes_list'):
        return True

    return False

def add_LList(message : Message) -> None:
    user_Form : dict = read_user(message.chat.id)
    if has_LList(message):
        return
    
    user_Form['likes_list'] = []
    update_user(message.chat.id, user_Form)

def add_TLList(message : Message, key : str) -> None:
    user_Form : dict = read_user(message.chat.id)
    if not has_LList(message):
        return
    
    if user_Form['likes_list'].__contains__(key):
        return
    
    user_Form['likes_list'].append(key)
    update_user(message.chat.id, user_Form)

def rem_FLList(message : Message, key : str) -> None:
    user_Form : dict = read_user(message.chat.id)
    if not has_LList(message):
        return
    
    user_Form['likes_list'].pop(key)
    update_user(message.chat.id, user_Form)



#Seen lists methods
def has_SList(message : Message) -> bool:
    user_Form : dict = read_user(message.chat.id)
    if user_Form.__contains__('seen_list'):
        return True

    return False

def has_SAll(message : Message) -> bool:
    user_Form : dict = read_user(message.chat.id)
    if not has_SList(message) :
        return False
    
    count : int = 0
    user_Keys : dict = clean_DB(message, get_DB())
    for key in user_Keys.keys():
        count += 1

    if user_Form['seen_list'].__len__() == count and user_Form['seen_list'].__len__() > 0 :
        return True
    
    return False

def in_SList(message : Message, key : str) -> bool:
    user_Form : dict = read_user(message.chat.id)
    if not has_SAll(message):
        return False
    
    if user_Form['seen_list'].__contains__(key):
        return True

    return False

def add_KTSList(message : Message, key : str) -> None:
    user_Form : dict = read_user(message.chat.id)

    if has_SAll(message):
        return
    
    if in_SList(message, key):
        return
    
    user_Form['seen_list'].append(key)
    update_user(message.chat.id, user_Form)
    return


#get cleaned DB methods
def clean_DB(message : Message, current_DB : dict) -> dict:
    user_Form : dict = read_user(message.chat.id)
    user_Gender : str = user_Form['Gender']
    target_Gender : str = user_Form['Preference']

    for key, value in current_DB.items():

        if (key == f'{message.chat.id}'):
            current_DB.pop(key)
            clean_DB(message, current_DB)
            break

        elif (current_DB[key]['Preference'] != user_Gender or user_Form['Preference'] != current_DB[key]['Gender']):# or (current_DB[key]['Preference'] != 'Ambos' and user_Form['Preference'] != 'Ambos'):
            current_DB.pop(key)
            clean_DB(message, current_DB)
            break
    
        print(f'ID:{key} \nDATA:{value}\n\n') if debug else True

    return current_DB

def get_RPList(message : Message) -> str:
    user_DB : dict = get_DB()
    user_DB = clean_DB(message, user_DB)

    key_list : list[str] = []
    for key in user_DB.keys():
        key_list.append(key) #type:ignore
    
    r_Value : int = random.randint(0, key_list.__len__() - 1)
    return key_list[r_Value]

def get_RProfile(message : Message, key : str) -> dict:
    user_DB : dict = get_DB()
    user_DB = clean_DB(message, user_DB)

    return user_DB[f'{key}']



def show_profiles(message : Message) -> None:
    new_KMarkup : InlineKeyboardMarkup = InlineKeyboardMarkup(row_width = 2)
    new_KMarkup.row(
        InlineKeyboardButton(text = '❤️', callback_data = 'profiles_like'),
        InlineKeyboardButton(text = '💌', callback_data = 'profiles_message')
    )
    new_KMarkup.row(
        InlineKeyboardButton(text = '💤', callback_data = 'profiles_next'),
        InlineKeyboardButton(text = '⚠️', callback_data = 'profiles_report')
    )
    new_KMarkup.add(InlineKeyboardButton(text = 'Atras', callback_data = 'profiles_back'))

    if not has_SList(message) :
        user_Form : dict = read_user(message.chat.id)
        user_Form['seen_list'] = []
        update_user(message.chat.id, user_Form)
        
    
    if has_SAll(message) :
        user_Form : dict = read_user(message.chat.id)
        user_Form['seen_list'] = []
        update_user(message.chat.id, user_Form)
        
    
    
    
    
    user_Form : dict = read_user(message.chat.id)
    key : str = get_RPList(message)



    while key in user_Form['seen_list']:
        key = get_RPList(message)


    display_Profile : dict = get_RProfile(message, key)

    add_KTSList(message, key)
    add_LList(message)

    if display_Profile['Photo'] != None:
        bot.send_photo(chat_id = message.chat.id, photo = display_Profile['Photo'])
        
    bot.send_message(
        chat_id = message.chat.id, 
        text = f'Nombre: {display_Profile['Name']} Edad: {display_Profile['Age']} \nDescripcion:\n**>>{display_Profile['Info']}',
        reply_markup = new_KMarkup,
        parse_mode = 'MarkdownV2'
    )
    @bot.callback_query_handler(lambda call : call.data.startswith('profiles_'))

    def handle_option(callback_Data : CallbackQuery) -> None:
        callback_Data.data = str(callback_Data.data).split('_')[1]
        user_Form : dict = read_user(callback_Data.message.chat.id)
        if callback_Data.data == 'like':
            handle_like(message, user_Form['seen_list'][user_Form['seen_list'].__len__() - 1])
            
        elif callback_Data.data == 'message':
            add_TLList(callback_Data.message, user_Form['seen_list'][user_Form['seen_list'].__len__() - 1])#type:ignore

            get_MSG = bot.send_message(chat_id = callback_Data.message.chat.id, text = f'Escriba a continuacion el mensaje que desea enviar')
            handle_like(message, user_Form['seen_list'][user_Form['seen_list'].__len__() - 1])
            bot.register_next_step_handler(get_MSG, handle_message, user_Form['seen_list'][user_Form['seen_list'].__len__() - 1])

        elif callback_Data.data == 'report':
            get_MSG = bot.send_message(chat_id = callback_Data.message.chat.id, text = f'Describa su motivo de reporte a continuacion')
            bot.register_next_step_handler(get_MSG, handle_report, user_Form['seen_list'][user_Form['seen_list'].__len__() - 1])

        elif callback_Data.data == 'next':
            show_profiles(callback_Data.message)#type:ignore
        
        elif callback_Data.data == 'back':
            bot.send_message(chat_id = callback_Data.message.chat.id, text = f'Saliendo del modo busqueda')
            return



def handle_like(message : Message, key : int) -> None:
    new_KMarkup : InlineKeyboardMarkup = InlineKeyboardMarkup(row_width = 3)
    new_KMarkup.row(
        InlineKeyboardButton('❤️', callback_data = 'request_like'),
        InlineKeyboardButton('💤', callback_data = 'request_next')
    )

    add_TLList(message, key)#type:ignore

    profile_Utils.bot = bot
    profile_Utils.show_profile(key, message.chat.id)
    tar_MSG : Message = bot.send_message(chat_id = int(key), text = f'Le has gustado al usuario {read_user(message.chat.id)['Name']}', reply_markup = new_KMarkup)
    
    @bot.callback_query_handler(lambda call : str(call.data).startswith('request_'))
    def handle_request(callback_Data : CallbackQuery) -> None:
        callback_Data.data = str(callback_Data.data).split('_')[1]

        if callback_Data.data == 'like':
            bot.send_message(chat_id = message.chat.id, text = f'{read_user(key)['Name']} ha aceptado tu solicitud\nUsuario:@{callback_Data.from_user.username}') #type:ignore
            bot.send_message(chat_id = key, text = f'{read_user(message.chat.id)['Name']} ha aceptado tu solicitud\nUsuario:@{message.from_user.username}') #type:ignore

        elif callback_Data.data == 'next':
            show_profiles(message)
            return
        
        bot.delete_message(chat_id = callback_Data.message.chat.id, message_id = tar_MSG.id)
        bot.delete_message(chat_id = message.chat.id, message_id = tar_MSG.id)

        return

def handle_message(message : Message, key : str) -> None:
    bot.send_message(chat_id = message.chat.id, text = 'Mensaje enviado')
    bot.send_message(chat_id = key, text = f'Mensaje de {read_user(message.chat.id)['Name']}:\n{message.text}')
    show_profiles(message)#type:ignore

def handle_report(message : Message, key : str) -> None:
    bot.send_message(chat_id = message.chat.id, text = f'Reporte enviado')
    for admin in get_admins():
        bot.send_message(chat_id = admin, text = f'Reporte del usuario:{read_user(message.chat.id)['Name']}\nSobre el usuario:{read_user(int(key))['Name']}\nInfo de reporte:\n{message.text}')