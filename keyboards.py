from telebot.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton


def keyboard(*buttons):
    keyboard = ReplyKeyboardMarkup(True)
    keyboard.row(*buttons)
    return keyboard


def trip_keyboard(*trips):
    keyboard = InlineKeyboardMarkup()
    for trip in trips:
        keyboard.add(InlineKeyboardButton(text=trip.get("title"), callback_data=f'trip:{trip.get("title")}'))
    return keyboard