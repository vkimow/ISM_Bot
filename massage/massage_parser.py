from classes.info import AboutUs, GlobalLinks, Paragraph
from classes.link import Link, LinkGroup
from google.google_parser import Parser
from google.google_download import Downloadable
from classes.services import Service, Specialist, Massage
from classes.education import Lesson, Course
from config import Paths
from classes.users import Admin
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

        def parse_about_paragraphs(sheet):
            paragraphs = []
            title_col = 0
            text_col = 1

            for row in sheet:
                title = row[title_col]
                text = row[text_col]

                paragraph = Paragraph(title, text)
                paragraphs.append(paragraph)

            return paragraphs

        def parse_about_links(sheet):
            links = []
            name_col = 0
            url_col = 1

            for row in sheet:
                name = row[name_col]
                url = row[url_col]

                link = Link(name, url)
                links.append(link)

            return LinkGroup('Ссылки', links)

        def parse_about_maps(sheet):
            map_links = []
            map_name_col = 0
            url_col = 1

            for row in sheet:
                map_name = row[map_name_col]
                url = row[url_col]

                map_link = Link(f'Открыть в {map_name}', url)
                map_links.append(map_link)

            return LinkGroup('Карты', map_links)

        def parse_links(sheet):
            education_link_row = 0

            education_link = sheet[education_link_row][1]

            return GlobalLinks(education_link)

        def get_sheet(name, start_col = '', end_col = '', start_row = ''):
            return self.__get_sheet(spreadsheet_id, name, start_col, end_col, start_row)

        links = parse_links(get_sheet('Ссылки', 'A', 'B', '1'))
        backgrounds_to_download = parse_backgrounds(get_sheet('Фон', 'A', 'C', '2'))
        about_paragraphs = parse_about_paragraphs(get_sheet('О Нас', 'A', 'B', '2'))
        about_links = parse_about_links(get_sheet('О Нас', 'D', 'E', '2'))
        about_maps = parse_about_maps(get_sheet('О Нас', 'G', 'H', '2'))
        about = AboutUs(about_paragraphs, about_links, about_maps)

        files_to_download = backgrounds_to_download
        return about, links, files_to_download


    def parse_education(self, spreadsheet_id):
        def parse_lessons(sheet, start_index):
            result = []
            name_row = start_index + 0
            link_row = start_index + 1
            phone_numbers_start_row = start_index + 2

            for col in sheet:
                name = col[name_row]
                link = col[link_row]
                phone_numbers = set()

                index = phone_numbers_start_row
                while index < len(col) and col[index]:
                    phone_number = col[index]
                    phone_number = Number.ToUnifiedStyleNumber(phone_number)
                    if(Number.IsUnifiedStyleNumber(phone_number)):
                        phone_numbers.add(phone_number)
                    index += 1

                lesson = Lesson(name, link, phone_numbers)
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
            result = []
            username_col = 0
            phone_number_col = 1

            for row in sheet:
                try:
                    username = row[username_col]
                except:
                    username = None

                try:
                    phone_number = row[phone_number_col]
                except:
                    phone_number = None

                phone_number = Number.ToUnifiedStyleNumber(phone_number)
                admin = Admin(username, phone_number)
                result.append(admin)

            return result

        def get_sheet(name, start_col = '', end_col = '', start_row = ''):
            return self.__get_sheet(spreadsheet_id, name, start_col, end_col, start_row)

        admins = parse_main(get_sheet('Админы', 'A', 'B', '2'))
        return admins
