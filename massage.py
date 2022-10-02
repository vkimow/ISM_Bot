class Massage:
    def __init__(self, specialists, lectures, anatomy):
        self.specialists = specialists
        self.lectures = lectures
        self.anatomy = anatomy

class Specialist:
    def __init__(self, name, surname, link):
        self.name = name
        self.surname = surname
        self.link = link

    def get_full_name(self):
        return f"{self.name} {self.surname}"

class Lecture:
    def __init__(self, name, link):
        self.name = name
        self.link = link

class Anatomy:
    def __init__(self, name, content):
        self.name = name
        self.content = content
