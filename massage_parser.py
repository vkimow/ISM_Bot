from google_sheet_parser import Parser
from massage import Massage, Specialist, Lecture, Anatomy

def parse(service, spreadsheetId):
    def parse_specialists(sheet):
        result = []
        name_col = 0
        surname_col = 1
        link_col = 2

        for row in sheet:
            name = row[name_col]
            surname = row[surname_col]
            link = row[link_col]

            specialist = Specialist(name, surname, link)
            result.append(specialist)

        return result

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
        name_col = 0
        description_col = 1

        for row in sheet:
            name = row[name_col]
            description = row[description_col]

            anatomy = Anatomy(name, description)
            result[anatomy.name] = anatomy

        return result

    def get_sheet(name, start_col = '', end_col = '', start_row = '', end_row = ''):
        google_sheet = Parser.get_google_sheet(service, spreadsheetId, name, start_col, end_col, start_row, end_row)
        return google_sheet['values']

    specialists = parse_specialists(get_sheet('Специалисты', 'A', 'C', '2'))
    lectures = parse_lectures(get_sheet('Лекции', 'A', 'B', '2'))
    anatomy = parse_anatomy(get_sheet('Анатомия', 'A', 'B', '2'))

    return Massage(specialists, lectures, anatomy)
