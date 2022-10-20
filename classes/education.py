from config import Paths

class Lesson:
    def __init__(self, name, link, numbers):
        self.name = name
        self.link = link
        self.numbers = numbers

class Course:
    def __init__(self, name, lessons):
        self.name = name
        self.lessons = lessons
        self.numbers = set()

        for lesson in self.lessons:
            self.numbers.union(lessons.numbers)
