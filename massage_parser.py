from classes.info import AboutUs, Paragraph, Links, MapLinks
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
        return google_sheet['values'] if 'values' in google_sheet else None


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

        def parse_about(sheet):
            paragraphs = []
            title_col = 0
            text_col = 1

            for row in sheet:
                title = row[title_col]
                text = row[text_col]

                paragraph = Paragraph(title, text)
                paragraphs.append(paragraph)

            return AboutUs(paragraphs)

        def parse_links(sheet):
            appointment_link_row = 0
            education_link_row = 1
            website_link_row = 2
            vk_group_link_row = 3
            map_gis_link_row = 4
            map_yandex_link_row = 5
            map_google_link_row = 6

            appointment_link = sheet[appointment_link_row][1]
            education_link = sheet[education_link_row][1]
            website_link = sheet[website_link_row][1]
            vk_group_link = sheet[vk_group_link_row][1]
            map_gis_link = sheet[map_gis_link_row][1]
            map_yandex_link = sheet[map_yandex_link_row][1]
            map_google_link = sheet[map_google_link_row][1]

            map_links = MapLinks(map_gis_link, map_yandex_link, map_google_link)
            return Links(appointment_link, education_link, website_link, vk_group_link, map_links)

        def get_sheet(name, start_col = '', end_col = '', start_row = ''):
            return self.__get_sheet(spreadsheet_id, name, start_col, end_col, start_row)

        backgrounds_to_download = parse_backgrounds(get_sheet('Фон', 'A', 'C', '2'))
        about = parse_about(get_sheet('О Нас', 'A', 'B', '2'))
        links = parse_links(get_sheet('Ссылки', 'A', 'B', '1'))

        files_to_download = backgrounds_to_download
        return about, links, files_to_download


    def parse_education(self, spreadsheet_id):
        def parse_lessons(sheet, start_index):
            result = []
            name_row = start_index + 0
            link_row = start_index + 1
            numbers_start_row = start_index + 2

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

        def parse_course(sheet):
            name_row = 0
            description_row = 1
            link_row = 2
            lessons_start_row = 3

            name = sheet[0][name_row]
            description = sheet[0][description_row]
            link = sheet[0][link_row]
            lessons = parse_lessons(sheet, lessons_start_row)

            return Course(name, description, link, lessons)

        def parse_courses(sheetsProperties):
            result = []

            for sheetProperties in sheetsProperties:
                name = sheetProperties['properties']['title']
                sheet = get_sheet(name, 'B', 'Z', '1')
                course = parse_course(sheet)
                result.append(course)

            return result

        def get_sheet(name, start_col = '', end_col = '', start_row = ''):
            return self.__get_sheet(spreadsheet_id, name, start_col, end_col, start_row, major_dimension = 'COLUMNS')

        courses = parse_courses(Parser.get_google_sheets_properties(self.services.sheets, spreadsheet_id))
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
            result = {}
            telegram_col = 0

            for row in sheet:
                telegram = row[telegram_col]
                admin = Admin(telegram)

                if telegram in result:
                    continue

                result[telegram] = admin

            return result

        def get_sheet(name, start_col = '', end_col = '', start_row = ''):
            return self.__get_sheet(spreadsheet_id, name, start_col, end_col, start_row)

        admins = parse_main(get_sheet('Админы', 'A', 'A', '2'))
        return admins


    def parse_users(self, spreadsheet_id):
        def parse_main(sheet):
            result = dict()
            user_id_col = 0
            name_col = 0
            number_col = 0

            if not sheet:
                return result

            for row in sheet:
                user_id = row[user_id_col]
                name = row[name_col]
                number = row[number_col]
                user = User(user_id, name, number)

                if user_id in result:
                    continue

                result[user_id] = user

            return result

        def get_sheet(name, start_col = '', end_col = '', start_row = ''):
            return self.__get_sheet(spreadsheet_id, name, start_col, end_col, start_row)

        users = parse_main(get_sheet('Пользователи', 'A', 'C', '2'))
        return users
