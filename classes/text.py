class Paragraph:
    def __init__(self, title, text):
        self.title = title
        self.text = text

    def get_text(self):
        result = ''

        if self.title:
            result += f'*{self.title}*'

        if self.text:
            result += '\n' if result else ''
            result += self.text

        return result
