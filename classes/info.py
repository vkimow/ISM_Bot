class AboutUs:
    def __init__(self, paragraphs):
        self.paragraphs = paragraphs

    def get_text(self):
        result = ''
        for paragraph in self.paragraphs:
            result += '\n\n' if result else ''
            result += f'*{paragraph.title}*\n'
            result += f'{paragraph.text}'

        return result


class Paragraph:
    def __init__(self, title, text):
        self.title = title
        self.text = text

class Links:
    def __init__(self, appointment, education, website, vk_group, map):
        self.appointment = appointment
        self.education = education
        self.website = website
        self.vk_group = vk_group
        self.map = map

class MapLinks:
    def __init__(self, gis, yandex, google):
        self.gis = gis
        self.yandex = yandex
        self.google = google
