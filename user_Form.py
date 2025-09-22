import json, telebot
from user_DB import STD_UserForm
from user_DB import create_user, read_user

from telebot.types import Message
from telebot.types import ReplyKeyboardMarkup
from telebot.types import ReplyKeyboardRemove

new_user : dict = STD_UserForm
bot : telebot.TeleBot



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

    get_pinfo(message)

def get_pinfo(message : Message) -> None:
    new_KMarkup : ReplyKeyboardMarkup = ReplyKeyboardMarkup(True, True, None, 1)
    new_KMarkup.add('Continuar')

    get_MSG = bot.send_message(chat_id = message.chat.id, text = f'Introduzca su informacion de perfil', reply_markup = new_KMarkup)
    bot.register_next_step_handler(get_MSG, set_pinfo)

def set_pinfo(message : Message) -> None:
    tar_MSG = bot.send_message(chat_id = message.chat.id, text = f'Espere un momento...', reply_markup = ReplyKeyboardRemove())
    new_user['Info'] = message.text if message.text != 'Continuar' else None #Ternary operator used
    bot.delete_message(chat_id = message.chat.id, message_id = tar_MSG.id)

    get_gender(message)

def get_gender(message : Message) -> None:
    new_KMarkup : ReplyKeyboardMarkup = ReplyKeyboardMarkup(True, True, None, 2)
    new_KMarkup.row('Masculino', 'Femenino')
    
    get_MSG = bot.send_message(chat_id = message.chat.id, text = f'Seleccione su genero a continuacion', reply_markup = new_KMarkup)
    bot.register_next_step_handler(get_MSG, set_gender)

def set_gender(message : Message) -> None:
    gender_List : list[str] = ['Masculino', 'Femenino']
    tar_MSG = bot.send_message(chat_id = message.chat.id, text = f'Espere un momento...', reply_markup = ReplyKeyboardRemove())

    if message.text not in gender_List:
        get_gender(message)
        return

    new_user['Gender'] = message.text

    bot.delete_message(chat_id = message.chat.id, message_id = tar_MSG.id)
    get_preference(message)

def get_preference(message : Message) -> None:
    new_KMarkup : ReplyKeyboardMarkup = ReplyKeyboardMarkup(True, True, None, 2)
    new_KMarkup.row('Masculino', 'Femenino')
    new_KMarkup.add('Ambos')
    
    get_MSG = bot.send_message(chat_id = message.chat.id, text = f'Seleccione su pareja ideal', reply_markup = new_KMarkup)
    bot.register_next_step_handler(get_MSG, set_preference)

def set_preference(message : Message) -> None:
    gender_List : list[str] = ['Masculino', 'Femenino', 'Ambos']
    tar_MSG = bot.send_message(chat_id = message.chat.id, text = f'Espere un momento...', reply_markup = ReplyKeyboardRemove())
    
    if message.text not in gender_List:
        get_preference(message)
        return

    new_user['Preference'] = message.text
    
    bot.delete_message(chat_id = message.chat.id, message_id = tar_MSG.id)
    get_picture(message)

def get_picture(message : Message) -> None:
    new_KMarkup : ReplyKeyboardMarkup = ReplyKeyboardMarkup(True, True, None, 1)
    new_KMarkup.add('Continuar')
    
    get_MSG = bot.send_message(chat_id = message.chat.id, text = f'Por ultimo envie una foto de perfil', reply_markup = new_KMarkup)
    bot.register_next_step_handler(get_MSG, set_picture)

def set_picture(message : Message) -> None:
    tar_MSG = bot.send_message(chat_id = message.chat.id, text = f'Espere un momento...', reply_markup = ReplyKeyboardRemove())

    try :
        if message.photo[0].file_id == None :# type: ignore
            bot.send_message(chat_id = message.chat.id, text = f'La imagen de perfil es obligatoria')
            get_picture(message)
            return
        
        new_user['Photo'] = message.photo[0].file_id # type: ignore
    
    except IndexError:
        pass

    except TypeError:
        pass

    bot.delete_message(chat_id = message.chat.id, message_id = tar_MSG.id)
    create_user(message.chat.id, new_user)
    bot.send_message(chat_id = message.chat.id, text = f'Su usuario ha sido creado bajo el nombre *{read_user(message.chat.id)['Name']}* y esta pendiente a aprobacion', parse_mode = 'MarkdownV2')