from google_parser import Parser
from google_download import Downloadable, get_drive_id_from_url
from massage import Massage, Specialist, Lecture, Anatomy
from config import Paths

def parse(services, spreadsheetId):

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

    def parse_lectures(sheet):
        result = []
        name_col = 0
        link_col = 1

        for row in sheet:
            name = row[name_col]
            link = row[link_col]

            lecture = Lecture(name, link)
            result.append(lecture)

        return result

    def parse_anatomy(sheet):
        result = {}
        photos_to_download = []
        name_col = 0
        description_col = 1
        info_link_col = 2
        photo_link_col = 3

        for row in sheet:
            name = row[name_col]
            description = row[description_col]
            info_link = row[info_link_col]

            anatomy = Anatomy(name, description, info_link)
            result[anatomy.name] = anatomy

            photo_link = row[photo_link_col]
            photo_to_download = Downloadable(photo_link, Paths.anatomy, anatomy.name, 'jpg')
            photos_to_download.append(photo_to_download)

        return result, photos_to_download

    def parse_actions(sheet):
        photos_to_download = []
        photo_link_col = 0
        index = 1

        for row in sheet:
            photo_link = row[photo_link_col]
            photo_to_download = Downloadable(photo_link, Paths.actions, f'Акция {index}', 'jpg')
            photos_to_download.append(photo_to_download)
            index += 1

        return photos_to_download

    def parse_backgrounds(sheet):
        photos_to_download = []
        name_col = 0
        photo_link_col = 2

        for row in sheet:
            name = row[name_col]
            photo_link = row[photo_link_col]
            photo_to_download = Downloadable(photo_link, Paths.backgrounds, name, 'jpg')
            photos_to_download.append(photo_to_download)

        return photos_to_download


    def get_sheet(name, start_col = '', end_col = '', start_row = '', end_row = ''):
        google_sheet = Parser.get_google_sheet(services.sheets, spreadsheetId, name, start_col, end_col, start_row, end_row)
        return google_sheet['values']

    specialists, specialists_downloads = parse_specialists(get_sheet('Специалисты', 'A', 'E', '2'))
    lectures = parse_lectures(get_sheet('Лекции', 'A', 'B', '2'))
    anatomy, anatomy_downloads = parse_anatomy(get_sheet('Анатомия', 'A', 'D', '2'))
    action_downloads = parse_actions(get_sheet('Акции', 'A', 'A', '2'))
    background_downloads = parse_backgrounds(get_sheet('Фон', 'A', 'C', '2'))

    massage = Massage(specialists, lectures, anatomy)
    files_to_download = specialists_downloads + anatomy_downloads + action_downloads + background_downloads
    return massage, files_to_download
