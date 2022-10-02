import telebot
from telebot import types

class Markup:
    remove = types.ReplyKeyboardRemove()

    class Main:
        show = types.ReplyKeyboardRemove()

    class Appointment:
        def main(specialists):
            result = types.InlineKeyboardMarkup()

            for specialist in specialists:
                button = types.InlineKeyboardButton(text = specialist.get_full_name(), url = specialist.link)
                result.add(button)

            result.add(types.InlineKeyboardButton(text = 'Отмена записи', callback_data='appointment cancel'))
            return result

    class Lectures:
        def main(lectures):
            result = types.InlineKeyboardMarkup()

            for lecture in lectures:
                button = types.InlineKeyboardButton(text = lecture.name, url = lecture.link)
                result.add(button)

            return result

    class Anatomy:
        def main(anatomy):
            result = types.InlineKeyboardMarkup()

            for name in anatomy:
                button = types.InlineKeyboardButton(text = name, callback_data=f'anatomy organ {name}')
                result.add(button)

            return result

        def back():
            result = types.InlineKeyboardMarkup()
            result.add(types.InlineKeyboardButton(text = 'Вернуться', callback_data='anatomy back'))
            return result
