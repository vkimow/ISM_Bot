class AboutUs:
    def __init__(self, paragraphs, links, maps):
        self.paragraphs = paragraphs
        self.links = links
        self.maps = maps

    def get_text(self):
        result = ''
        for paragraph in self.paragraphs:
            result += '\n\n' if result else ''
            result += paragraph.get_text()

        return result

class GlobalLinks:
    def __init__(self, education):
        self.education = education
