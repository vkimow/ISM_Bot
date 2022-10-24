from config import Paths

class Lesson:
    def __init__(self, name, link, numbers):
        self.name = name
        self.link = link
        self.numbers = numbers

class Course:
    def __init__(self, name, description, link, lessons):
        self.name = name
        self.description = description
        self.link = link
        self.lessons = lessons
        self.numbers = set()

        for lesson in self.lessons:
            self.numbers.update(lesson.numbers)

    def get_text(self):
        result = f'*{self.name}*\n'
        result += f'{self.description}'
        return result
