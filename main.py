import telebot, os, json
import user_Utils, menu_Panel

from user_Utils import STD_Set

from telebot.types import Message

bot : telebot.TeleBot = telebot.TeleBot('6402990173:AAFty3Z7TuSzuDdjkmoModOn3J8kMAhFM-I')
std_F : str = 'MarkdownV2'

@bot.message_handler(commands = ['start'])
def handle_Start(message : Message) -> None:
    bot.send_message(message.chat.id, f'Welcome to love findr')

    if user_Utils.has_user(message.chat.id):
        bot.send_message(message.chat.id, f'User alredy created by the name *{user_Utils.get_user(message.chat.id)['name']}*', parse_mode = std_F)
        return
    
    data_Set : dict = STD_Set
  
    def set_Name(message : Message) -> None:
        if str(message.text).__len__() == 0:
            bot.send_message(message.chat.id, f'Your name cannot be blank')
            handle_Start(message)

        data_Set['name'] = message.text
        user_Utils.create_user(message.chat.id, data_Set)
        bot.send_message(message.chat.id, f'User created by the name *{user_Utils.get_user(message.chat.id)['name']}*', parse_mode = std_F)
        

    get : Message = bot.send_message(message.chat.id, f'Let\'s create your account, tell us your name (or alias)')
    bot.register_next_step_handler(get, set_Name)

os.system('clear')
print("DEBUG START")
bot.infinity_polling()
print("DEBUG END")