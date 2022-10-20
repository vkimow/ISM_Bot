from google_parser import Parser
from google_download import Downloadable
from classes.services import Service, Specialist, Massage
from classes.education import Lesson, Course
from config import Paths
from classes.users import Admin, User
from classes.number import Number


class MassageParser:
    def __init__(self, services):
        self.services = services

    def __get_sheet(self, spreadsheet_id, name, start_col = '', end_col = '', start_row = '', end_row = '', major_dimension = 'ROWS'):
        google_sheet = Parser.get_google_sheet(self.services.sheets, spreadsheet_id, name, start_col, end_col, start_row, end_row, major_dimension)
        return google_sheet['values']


    def parse_info(self, spreadsheet_id):
        def parse_backgrounds(sheet):
            result = []
            name_col = 0
            link_col = 2

            for row in sheet:
                name = row[name_col]
                link = row[link_col]

                background = Downloadable(link, Paths.backgrounds, name, 'jpg')
                result.append(background)

            return result

        def parse_about_us(sheet):
            return

        def get_sheet(name, start_col = '', end_col = '', start_row = ''):
            return self.__get_sheet(spreadsheet_id, name, start_col, end_col, start_row)

        backgrounds_to_download = parse_backgrounds(get_sheet('Фон', 'A', 'C', '2'))
        # about_us = parse_about_us(get_sheet('Лекции', 'A', 'B', '2'))

        files_to_download = backgrounds_to_download
        return files_to_download


    def parse_education(self, spreadsheet_id):
        def parse_lessons(sheet):
            result = []
            name_row = 0
            link_row = 1
            numbers_start_row = 2

            for col in sheet:
                name = col[name_row]
                link = col[link_row]
                numbers = set()

                index = numbers_start_row
                while index < len(col) and col[index]:
                    numberText = col[index]
                    numberText = Number.ToUnifiedStyleNumber(numberText)
                    if(Number.IsUnifiedStyleNumber(numberText)):
                        numbers.add(numberText)
                    index += 1

                lesson = Lesson(name, link, numbers)
                result.append(lesson)

            return result

        def parse_course(sheets):
            result = []

            for sheet in sheets:
                name = sheet['properties']['title']
                lessons = parse_lessons(sheet['values'])
                course = Course(name, lessons)
                result.append(course)

            return result

        courses = parse_course(Parser.get_google_sheets(self.services, spreadsheet_id))
        return courses


    def parse_massage(self, spreadsheet_id):
        def parse_actions(sheet):
            result = []
            link_col = 0
            index = 1

            for row in sheet:
                link = row[link_col]
                action = Downloadable(link, Paths.actions, f'Акция {index}', 'jpg')
                result.append(action)
                index += 1

            return result

        def parse_specialists(sheet):
            result = []
            photos_to_download = []
            name_col = 0
            surname_col = 1
            description_col = 2
            appointment_link_col = 3
            photo_link_col = 4

            for row in sheet:
                name = row[name_col]
                surname = row[surname_col]
                description = row[description_col]
                appointment_link = row[appointment_link_col]

                specialist = Specialist(name, surname, description, appointment_link)
                result.append(specialist)

                photo_link = row[photo_link_col]
                photo_to_download = Downloadable(photo_link, Paths.specialists, specialist.get_full_name(), 'jpg')
                photos_to_download.append(photo_to_download)

            return result, photos_to_download

        def parse_services(sheet):
            result = []
            name_col = 0
            link_col = 1

            for row in sheet:
                name = row[name_col]
                link = row[link_col]

                service = Service(name, link)
                result.append(service)

            return result

        def get_sheet(name, start_col = '', end_col = '', start_row = ''):
            return self.__get_sheet(spreadsheet_id, name, start_col, end_col, start_row)

        actions_to_download = parse_actions(get_sheet('Акции', 'A', 'A', '2'))
        specialists, photos_to_download = parse_specialists(get_sheet('Специалисты', 'A', 'E', '2'))
        services = parse_services(get_sheet('Услуги', 'A', 'B', '2'))

        massage = Massage(specialists, services)
        files_to_download = actions_to_download + photos_to_download

        return massage, files_to_download


    def parse_admins(self, spreadsheet_id):
        def parse_main(sheet):
            result = []
            telegram_col = 0

            for row in sheet:
                telegram = row[telegram_col]
                admin = Admin(telegram)
                result.append(admin)

            return result

        def get_sheet(name, start_col = '', end_col = '', start_row = ''):
            return self.__get_sheet(spreadsheet_id, name, start_col, end_col, start_row)

        admins = parse_main(get_sheet('Админы', 'A', 'A', '2'))
        return admins


    def parse_users(self, spreadsheet_id):
        def parse_main(sheet):
            result = []
            user_id_col = 0
            name_col = 0
            number_col = 0

            for row in sheet:
                user_id = row[user_id_col]
                name = row[name_col]
                number = row[number_col]

                user = User(user_id, name, number)
                result.append(user)

            return result

        def get_sheet(name, start_col = '', end_col = '', start_row = ''):
            return self.__get_sheet(spreadsheet_id, name, start_col, end_col, start_row)

        users = parse_main(get_sheet('Пользователи', 'A', 'C', '2'))
        return users
