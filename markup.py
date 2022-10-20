from telebot import types

class Markup:
    remove = types.ReplyKeyboardRemove()

    class Main:
        show = types.ReplyKeyboardRemove()

    class Services:
        def main():
            result = types.InlineKeyboardMarkup(row_width = 1)
            actions = types.InlineKeyboardButton(text = 'Акции', callback_data='services actions')
            specialist = types.InlineKeyboardButton(text = 'Записаться к специалисту', callback_data='services specialist')
            all_services = types.InlineKeyboardButton(text = 'Все услуги', callback_data='services all_services')
            result.add(actions, specialist, all_services)
            return result

    class Specialist:
        def list(specialists):
            result = types.InlineKeyboardMarkup(row_width = 1)

            for i in range(len(specialists)):
                button = types.InlineKeyboardButton(text = specialists[i].get_full_name(), callback_data=f'specialist appointment {i}')
                result.add(button)

            cancel = types.InlineKeyboardButton(text = 'Отмена записи', callback_data='appointment cancel')
            result.add(cancel)
            return result

        def concrete(specialist):
            result = types.InlineKeyboardMarkup(row_width = 1)
            appointment = types.InlineKeyboardButton(text = 'Записаться', url = specialist.appointment_link)
            back = types.InlineKeyboardButton(text = 'Вернуться', callback_data='specialist back')
            result.add(appointment, back)
            return result

    class Education:
        def main(programmes):
            result = types.InlineKeyboardMarkup(row_width = 1)

            for program in programmes:
                button = types.InlineKeyboardButton(text = program.name, callback_data=f'education program {program.name}')
                result.add(button)


            return result

        def program(program):
            result = types.InlineKeyboardMarkup(row_width = 1)

            for lesson in program.lessons:
                button = types.InlineKeyboardButton(text = lesson.name, url = lesson.url)
                result.add(button)

            back = types.InlineKeyboardButton(text = 'Вернуться', callback_data='education main')
            result.add(back)
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
    