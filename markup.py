from telebot import types

class Markup:
    remove = types.ReplyKeyboardRemove()

    class Main:
        show = types.ReplyKeyboardRemove()

    class GetContact:
        def main():
            result = types.ReplyKeyboardMarkup(row_width = 1)
            send_phone_number = types.KeyboardButton(text = 'Отправить номер', request_contact = True)
            cancel = types.KeyboardButton(text = 'Отмена')

            result.add(send_phone_number, cancel)
            return result

    class About:
        def main(links):
            result = types.InlineKeyboardMarkup(row_width = 1)
            map = types.InlineKeyboardButton(text = 'Открыть на карте', callback_data='about maps')
            vk = types.InlineKeyboardButton(text = 'Группа Вконтакте', url = links.vk_group)
            website = types.InlineKeyboardButton(text = 'Наш сайт', url = links.website)

            result.add(map, vk, website)
            return result

        def maps(links):
            result = types.InlineKeyboardMarkup(row_width = 1)
            map_2gis = types.InlineKeyboardButton(text = 'Открыть в 2GIS', url = links.map.gis)
            map_yandex = types.InlineKeyboardButton(text = 'Открыть в Яндекс Картах', url = links.map.yandex)
            map_google = types.InlineKeyboardButton(text = 'Открыть в Google Картах', url = links.map.google)
            back = types.InlineKeyboardButton(text = 'Вернуться', callback_data='about main')

            result.add(map_2gis, map_yandex, map_google, back)
            return result


    class Services:
        def main():
            result = types.InlineKeyboardMarkup(row_width = 1)
            actions = types.InlineKeyboardButton(text = 'Акции', callback_data='services actions')
            specialist = types.InlineKeyboardButton(text = 'Записаться к специалисту', callback_data='services specialist')
            all_services = types.InlineKeyboardButton(text = 'Все услуги', callback_data='services all_services')
            result.add(actions, specialist, all_services)
            return result

        def services_list(services):
            result = types.InlineKeyboardMarkup(row_width = 1)
            for service in services:
                button = types.InlineKeyboardButton(text = service.name, url = service.link)
                result.add(button)

            back = types.InlineKeyboardButton(text = 'Вернуться', callback_data='services main')
            result.add(back)
            return result

        def specialists_list(specialists):
            result = types.InlineKeyboardMarkup(row_width = 1)

            for i in range(len(specialists)):
                button = types.InlineKeyboardButton(text = specialists[i].get_full_name(), callback_data=f'specialist concrete {i}')
                result.add(button)

            cancel = types.InlineKeyboardButton(text = 'Вернуться', callback_data='services main')
            result.add(cancel)
            return result

    class Specialist:
        def concrete(specialist):
            result = types.InlineKeyboardMarkup(row_width = 1)
            appointment = types.InlineKeyboardButton(text = 'Записаться', url = specialist.appointment_link)
            back = types.InlineKeyboardButton(text = 'Вернуться', callback_data='specialist back')
            result.add(appointment, back)
            return result

    class Education:
        def main(courses, links):
            result = types.InlineKeyboardMarkup(row_width = 1)

            for i in range(len(courses)):
                button = types.InlineKeyboardButton(text = courses[i].name, callback_data=f'education course {i}')
                result.add(button)

            education = types.InlineKeyboardButton(text = 'Записаться на обучение', url = links.education)
            result.add(education)
            return result

        def course(course, lessons):
            result = types.InlineKeyboardMarkup(row_width = 1)

            for lesson in lessons:
                button = types.InlineKeyboardButton(text = lesson.name, url = lesson.link)
                result.add(button)

            if course.link:
                appointment = types.InlineKeyboardButton(text = 'Записаться', url = course.link)
                result.add(appointment)

            back = types.InlineKeyboardButton(text = 'Вернуться', callback_data='education main')
            result.add(back)
            return result
