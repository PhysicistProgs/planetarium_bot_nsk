class Event:
    def __init__(self, title, description, date, url):
        self.title = self._fix_text(title)
        self.description = self._fix_text(description)
        self.date = date
        self.url = url

    def _fix_text(self, text):
        text = text.strip()
        text = text.replace("\n\n", "\n")
        text = text.replace('Подробнее', '')
        return text

    def get_text(self):
        return f'**{self.title}** {self.date}\n{self.description}\n\n[Подробнне]({self.url})'
