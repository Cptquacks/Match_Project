import telebot

from telebot.types import Message

from telebot.types import ReplyKeyboardMarkup
from telebot.types import KeyboardButton
from telebot.types import ReplyKeyboardRemove

class menu_Panel:
    bot : telebot.TeleBot
    panel : ReplyKeyboardMarkup

    options : list[tuple] = [
        ('🔍 Search', None),
        ('👤 Profile', None),
        ('⚙️ Search Settings', None)
    ]

    def __init__(self, bot : telebot.TeleBot) -> None:
        self.bot = bot
        self.panel = self.create_Panel()

    def create_Panel(self) -> ReplyKeyboardMarkup:
        optionsPanel : ReplyKeyboardMarkup = ReplyKeyboardMarkup(True, False, input_field_placeholder = '')

        optionsPanel.add(
            KeyboardButton(text = '🔍 Search'), KeyboardButton(text = '👤 Profile'), row_width = 2
        )
        optionsPanel.add(
            KeyboardButton(text = '⚙️ Search Settings'), row_width = 1
        )
        return optionsPanel
    
    def is_option(self, message : Message) -> bool:
        for element in  self.options:
            if (element[0] == message.text):
                print(element[0])

        return False
