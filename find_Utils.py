import json, telebot, random

from user_DB import read_user, get_DB, update_user

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
        InlineKeyboardButton(text = '❤️', callback_data = 'like'),
        InlineKeyboardButton(text = '💌', callback_data = 'message')
    )
    new_KMarkup.row(
        InlineKeyboardButton(text = '💤', callback_data = 'next'),
        InlineKeyboardButton(text = '⚠️', callback_data = 'report')
    )
    new_KMarkup.add(InlineKeyboardButton(text = 'Atras', callback_data = 'back'))

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
    bot.register_callback_query_handler(handle_option, lambda func : True)

def handle_option(callback_Data : CallbackQuery) -> None:
    user_Form : dict = read_user(callback_Data.message.chat.id)
    if callback_Data.data == 'like':
        add_TLList(callback_Data.message, user_Form['seen_list'][user_Form['seen_list'].__len__() - 1])#type:ignore
        show_profiles(callback_Data.message)#type:ignore
        
    elif callback_Data.data == 'message':
        add_TLList(callback_Data.message, user_Form['seen_list'][user_Form['seen_list'].__len__() - 1])#type:ignore
        show_profiles(callback_Data.message)#type:ignore

    elif callback_Data.data == 'next':
        show_profiles(callback_Data.message)#type:ignore
    
    elif callback_Data.data == 'back':
        return


