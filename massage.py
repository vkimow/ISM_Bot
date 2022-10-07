from distutils import extension
from config import Paths

class Massage:
    def __init__(self, specialists, lectures, anatomy):
        self.specialists = specialists
        self.lectures = lectures
        self.anatomy = anatomy

class Specialist:
    def __init__(self, name, surname, description, appointment_link):
        self.name = name
        self.surname = surname
        self.description = description
        self.appointment_link = appointment_link

    def get_full_name(self):
        return f'{self.name} {self.surname}'

    def get_photo_path(self):
        return f'{Paths.specialists}/{self.get_full_name()}.jpg'

    def get_full_description(self):
        return f'*{self.get_full_name()}*\n'\
                f'{self.description}'

class Lecture:
    def __init__(self, name, link):
        self.name = name
        self.link = link

class Anatomy:
    def __init__(self, name, content, info_link):
        self.name = name
        self.content = content
        self.info_link = info_link if info_link else None