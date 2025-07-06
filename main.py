import telebot, os, json

bot : telebot.TeleBot = telebot.TeleBot('6402990173:AAFty3Z7TuSzuDdjkmoModOn3J8kMAhFM-I')

@bot.message_handler(commands = ['start'])
def handle_Start(message) -> None:
    bot.send_message(message.chat.id, f'Hello')

os.system('clear')
print("DEBUG START")
bot.infinity_polling()
print("DEBUG END")