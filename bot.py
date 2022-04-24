import configparser

import telebot

from hadlers import add_handlers

CONFIG = configparser.ConfigParser()
CONFIG.read('config.ini')
TOKEN = CONFIG.get('token', 'token')
bot = telebot.TeleBot(TOKEN)


if __name__ == '__main__':
    add_handlers(bot)
    bot.infinity_polling()
