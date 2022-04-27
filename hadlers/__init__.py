from typing import Optional

import telebot
from apps.planetarium import get_planetarium_contacts, get_planetarium_news


class RootMarkup(telebot.types.ReplyKeyboardMarkup):
    """Root markup containing two main buttons"""

    news_text = 'Последние новости'
    contacts_text = 'Контакты'
    btn_show_news = telebot.types.KeyboardButton(news_text)
    btn_show_contacts = telebot.types.KeyboardButton(contacts_text)

    def __init__(
        self,
        resize_keyboard: Optional[bool] = None,
        one_time_keyboard: Optional[bool] = None,
        selective: Optional[bool] = None,
        row_width: int = 3,
        input_field_placeholder: Optional[str] = None,
    ):
        super().__init__(
            resize_keyboard, one_time_keyboard, selective, row_width, input_field_placeholder
        )
        self.add(self.btn_show_news, self.btn_show_contacts)


root_markup = RootMarkup(resize_keyboard=True)


def add_handlers(bot: telebot.TeleBot):
    """Add handlers to bot"""

    @bot.message_handler(commands=['start'])
    def start(message):
        bot.send_message(
            chat_id=message.chat.id, text='Привет! Что тебя интересует?', reply_markup=root_markup
        )

    @bot.message_handler(content_types='text')
    def response(message):
        if message.text == root_markup.news_text:
            news_all = get_planetarium_news()
            for news in news_all:
                bot.send_message(
                    chat_id=message.chat.id,
                    text=news.get_text(),
                    reply_markup=root_markup,
                    parse_mode='Markdown',
                )
        elif message.text == root_markup.contacts_text:
            schedule = get_planetarium_contacts()
            bot.send_message(chat_id=message.chat.id, text=schedule, reply_markup=root_markup)
        else:
            bot.send_message(
                chat_id=message.chat.id,
                text='Я не знаю такую команду :(',
                reply_markup=root_markup,
            )
