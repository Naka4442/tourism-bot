from telebot.types import ReplyKeyboardMarkup


def keyboard(*buttons):
    keyboard = ReplyKeyboardMarkup(True)
    keyboard.row(*buttons)
    return keyboard