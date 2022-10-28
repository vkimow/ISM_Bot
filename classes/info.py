class AboutUs:
    def __init__(self, paragraphs, links, maps):
        self.paragraphs = paragraphs
        self.links = links
        self.maps = maps

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


class GlobalLinks:
    def __init__(self, education):
        self.education = education
