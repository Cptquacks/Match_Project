import telebot, profile_Utils

from bot import bot
from user_DB import get_DB, read_user, update_user
from admin_Utils import get_admins

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot.types import Message, CallbackQuery

user_DB : dict


def get_user(user_ID : int) -> dict:
    user_Form : dict = read_user(user_ID)
    
    if not user_Form.__contains__('seen_list'):
        user_Form['seen_list'] = []
        update_user(user_ID, user_Form)

    if not user_Form.__contains__('like_list'):
        user_Form['like_list'] = []
        update_user(user_ID, user_Form)
    
    return user_Form

def get_profile(user_Form : dict) -> dict:
    seen_List : list[str] = user_Form['seen_list']
    user_Gender : str = user_Form['Gender']
    user_Preference : str = user_Form['Preference']

    for key, value in user_DB.items():

        if (key not in seen_List):
            
            if (user_Gender != user_DB[key]['Gender'] and user_Preference != user_DB[key]['Preference']):
                profile_Data : dict = user_DB[key]
                profile_Data['key'] = key
                print(f'\tPID: {profile_Data['key']}')
                return profile_Data

            elif (user_Preference == 'Ambos' and user_DB[key]['Preference'] == 'Ambos'):
                profile_Data : dict = user_DB[key]
                profile_Data['key'] = key
                print(f'\tPID: {profile_Data['key']}')
                return profile_Data
    
    return {'error' : 'unknown'}

def slist_sall(user_Form : dict) -> bool:
    user_Gender : str = user_Form['Gender']
    user_Preference : str = user_Form['Preference']

    kCount : int = 0
    
    try:
        for key, value in user_DB.items():

            if (user_Gender != user_DB[key]['Gender'] and user_Preference != user_DB[key]['Preference']):
                kCount += 1

            elif (user_Preference == 'Ambos' and user_DB[key]['Preference'] == 'Ambos'):
                kCount += 1
    
    except NameError:
        return False

    if kCount != 0 and kCount == user_Form['seen_list'].__len__():
        return True
    
    return False

def slist_akey(user_Form : dict, key : int) -> dict:
    if slist_sall(user_Form):
        return user_Form
    
    user_Form['seen_list'].append(f'{key}')
    return user_Form

def slist_glast(user_Form : dict) -> int:
    return user_Form['seen_list'][user_Form['seen_list'].__len__() - 1]





def show_profiles(user_ID : int) -> None:
    user_Form : dict = get_user(user_ID)

    if slist_sall(user_Form):
        user_Form['seen_list'] = []
        update_user(user_ID, user_Form)



    profile_Form : dict = get_profile(user_Form)
    max_Tries : int = 300

    while profile_Form.__contains__('error') or profile_Form['key'] in user_Form['seen_list']:
        profile_Form = get_profile(user_Form)
        

        if max_Tries <= 300:
            bot.send_message(chat_id = user_ID, text = 'No se encontraron perfiles')
            return
        
        max_Tries -= 1


    new_KMarkup : InlineKeyboardMarkup = InlineKeyboardMarkup(row_width = 2)
    new_KMarkup.row(
        InlineKeyboardButton(text = '❤️', callback_data = f'profiles_like_{profile_Form['key']}'),
        InlineKeyboardButton(text = '💌', callback_data = f'profiles_message')
    )
    new_KMarkup.row(
        InlineKeyboardButton(text = '💤', callback_data = f'profiles_next'),
        InlineKeyboardButton(text = '⚠️', callback_data = 'fprofiles_report')
    )
    new_KMarkup.add(
        InlineKeyboardButton(text = 'Atras', callback_data = 'profiles_back')
    )
    
    if profile_Form['Photo'] != None:
        bot.send_photo(
            chat_id = user_ID,
            photo = profile_Form['Photo'],
            caption = (
                f'Nombre: {profile_Form['Name']}\n'
                f'Edad: {profile_Form['Age']}\n'
                f'Descripcion:\n**>>{profile_Form['Info']}'
            ),
            reply_markup = new_KMarkup,
            parse_mode = 'MarkdownV2'
            
        )
    
    elif profile_Form['Photo'] == None:
        bot.send_message(
            chat_id = user_ID,
            text = (
                f'Nombre: {profile_Form['Name']}\n'
                f'Edad: {profile_Form['Age']}\n'
                f'Descripcion:\n**>>{profile_Form['Info']}'
            ),
            reply_markup = new_KMarkup,
            parse_mode = 'MarkdownV2'
            
        )

    user_Form = slist_akey(user_Form, profile_Form['key'])
    update_user(user_ID, user_Form)
    print(profile_Form['key'])

@bot.callback_query_handler(lambda call : str(call.data).startswith('profiles_'))
def handle_request(callback_Data : CallbackQuery) -> None:
    data : str = str(callback_Data.data).split('_')[1]
        
    if data == 'like':
        key : str = str(callback_Data.data).split('_')[2]
        handle_like(
            callback_Data.message, #type: ignore
            slist_glast(read_user(
                callback_Data.message.chat.id
            ))
        )#type: ignore

    elif data == 'next':
        show_profiles(callback_Data.message.chat.id)

def handle_like(message : Message, key : int) -> None:
    user_ID : int = message.chat.id
    show_profiles(user_ID)

    new_KMarkup : InlineKeyboardMarkup = InlineKeyboardMarkup(row_width = 3)
    new_KMarkup.row(
        InlineKeyboardButton('❤️', callback_data = f'request-like-{message.chat.id}'),#type: ignore
        InlineKeyboardButton('💤', callback_data = f'request-next')
    )


    profile_Utils.bot = bot
    profile_Utils.show_profile(key, user_ID)
    bot.send_message(chat_id = key, text = f'Le has gustado al usuario {read_user(user_ID)['Name']}', reply_markup = new_KMarkup)
    
@bot.callback_query_handler(lambda call : str(call.data).startswith('request-'))
def handle_reponse(callback_Data : CallbackQuery) -> None:
    order = str(callback_Data.data).split('-')[1]

    target_ID : int = callback_Data.message.chat.id

    if order == 'like':
        request_ID : int = int(str(callback_Data.data).split('-')[2])

 

        bot.send_message(chat_id = request_ID, text = f'Has hecho un match con {read_user(target_ID)['Name']} \nUsuario:@{read_user(target_ID)['Username']}') #type:ignore
        bot.send_message(chat_id = target_ID, text = f'Has hecho un match con {read_user(request_ID)['Name']} \nUsuario:@{read_user(request_ID)['Username']}') #type:ignore
            

    elif order == 'next':
        pass
        
    show_profiles(target_ID)