class News:
    def __init__(self, text, date, url):
        self.text = self._fix_text(text)
        self.date = date
        self.url = url

    def _fix_text(self, text):
        text = text.strip()
        text = text.replace("\n\n", "\n")
        return text

    def get_text(self):
        news_text = f'{self.text}\n\n[Новость на сайте]({self.url})'
        return news_text
