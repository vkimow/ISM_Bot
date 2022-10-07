import telebot
from telebot import types

class Markup:
    remove = types.ReplyKeyboardRemove()

    class Main:
        show = types.ReplyKeyboardRemove()

    class Appointment:
        def main(specialists):
            result = types.InlineKeyboardMarkup(row_width = 1)

            for i in range(len(specialists)):
                button = types.InlineKeyboardButton(text = specialists[i].get_full_name(), callback_data=f'appointment specialist {i}')
                result.add(button)

            cancel = types.InlineKeyboardButton(text = 'Отмена записи', callback_data='appointment cancel')
            result.add(cancel)
            return result

        def specialist(specialist):
            result = types.InlineKeyboardMarkup(row_width = 1)
            appointment = types.InlineKeyboardButton(text = 'Записаться', url = specialist.appointment_link)
            back = types.InlineKeyboardButton(text = 'Вернуться', callback_data='specialist back')
            result.add(appointment, back)
            return result

    class Lectures:
        def main(lectures):
            result = types.InlineKeyboardMarkup(row_width = 1)

            for lecture in lectures:
                button = types.InlineKeyboardButton(text = lecture.name, url = lecture.link)
                result.add(button)

            return result

    class Anatomy:
        def main(anatomy):
            result = types.InlineKeyboardMarkup(row_width = 1)

            for name in anatomy:
                button = types.InlineKeyboardButton(text = name, callback_data=f'anatomy organ {name}')
                result.add(button)

            return result

        def organ(organ):
            result = types.InlineKeyboardMarkup(row_width = 1)

            if(organ.info_link):
                info = types.InlineKeyboardButton(text = 'Подробнее', url = organ.info_link)
                result.add(info)

            back = types.InlineKeyboardButton(text = 'Вернуться', callback_data='organ back')
            result.add(back)
            return result
