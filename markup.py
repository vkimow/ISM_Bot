from telebot import types

class Markup:
    remove = types.ReplyKeyboardRemove()

    @staticmethod
    def link(link):
        return types.InlineKeyboardButton(text = link.name, url = link.url)

    @staticmethod
    def link_group(link_group):
        result = []
        for link in link_group.links:
            result.append(Markup.link(link))
        return result

    class Main:
        show = types.ReplyKeyboardRemove()

    class Admin:
        def main():
            result = types.InlineKeyboardMarkup(row_width = 1)
            refresh = types.InlineKeyboardButton(text = 'Обновить инфомрацию', callback_data='admin refresh')
            forward_message = types.InlineKeyboardButton(text = 'Распространить сообщение', callback_data='admin forward')

            result.add(refresh, forward_message)
            return result

        def refresh():
            result = types.InlineKeyboardMarkup(row_width = 1)
            all = types.InlineKeyboardButton(text = 'Обновить все', callback_data='refresh all')
            admins = types.InlineKeyboardButton(text = 'Обновить список админов', callback_data='refresh admins')
            back = types.InlineKeyboardButton(text = 'Вернуться', callback_data='admin main')

            result.add(all, admins, back)
            return result

        def forward():
            result = types.InlineKeyboardMarkup(row_width = 2)
            accept = types.InlineKeyboardButton(text = 'Отправить', callback_data='forward accept')
            cancel = types.InlineKeyboardButton(text = 'Отмена', callback_data='forward cancel')

            result.add(accept, cancel)
            return result

    class GetContact:
        def main():
            result = types.ReplyKeyboardMarkup(row_width = 1)
            send_phone_number = types.KeyboardButton(text = 'Отправить номер', request_contact = True)
            cancel = types.KeyboardButton(text = 'Отмена')

            result.add(send_phone_number, cancel)
            return result

    class About:
        def main(about):
            result = types.InlineKeyboardMarkup(row_width = 1)
            map = types.InlineKeyboardButton(text = 'Открыть на карте', callback_data='about maps')
            result.add(map)

            for link in Markup.link_group(about.links):
                result.add(link)

            return result

        def maps(about):
            result = types.InlineKeyboardMarkup(row_width = 1)


            for link in Markup.link_group(about.maps):
                result.add(link)

            back = types.InlineKeyboardButton(text = 'Вернуться', callback_data='about main')
            result.add(back)
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

    class Action:
        def concrete(action):
            result = types.InlineKeyboardMarkup(row_width = 1)
            link = types.InlineKeyboardButton(text = 'Открыть на сайте', url = action.link)
            result.add(link)
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
