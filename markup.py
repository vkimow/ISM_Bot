import telebot
from telebot import types

class Buttons:
    class General:
        cancel = types.InlineKeyboardButton(text='Отмена', callback_data='cancel')

class Markup:
    remove = types.ReplyKeyboardRemove()

    class Main:
        show = types.ReplyKeyboardRemove()
