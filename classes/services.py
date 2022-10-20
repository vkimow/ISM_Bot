from config import Paths

class Massage:
    def __init__(self, specialists, services):
        self.specialists = specialists
        self.services = services

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

class Service:
    def __init__(self, name, link):
        self.name = name
        self.link = link
