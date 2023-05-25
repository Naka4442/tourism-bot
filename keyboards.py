from telebot.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime, timedelta


def keyboard(*buttons):
    keyboard = ReplyKeyboardMarkup(True)
    keyboard.row(*buttons)
    return keyboard

def date_keyboard():
    keyboard = InlineKeyboardMarkup()
    row = []
    k = int(datetime.now().strftime("%w"))
    weekdays = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
    for i in range(7):
        row.append(InlineKeyboardButton(text=weekdays[i], callback_data=" "))
    keyboard.row(*row)
    row.clear()
    if k != 1:
        for i in range(k - 1):
            row.append(InlineKeyboardButton(text=" ", callback_data=" "))
    for i in range(30):
        d = datetime.now() + timedelta(days=i)
        row.append(InlineKeyboardButton(text=d.strftime("%d.%m"), callback_data=f"date:offset {i}"))
        if k >= 7 or i == 29:
            k = 0
            if len(row) < 7:
                for j in range(7 - len(row)):
                    row.append(InlineKeyboardButton(text=" ", callback_data="    "))
            keyboard.row(*row)
            row.clear()
        k += 1
    return keyboard

def trip_keyboard(*trips):
    keyboard = InlineKeyboardMarkup()
    for trip in trips:
        keyboard.add(InlineKeyboardButton(text=trip.get("title"), callback_data=f'trip:{trip.get("title")}'))
    return keyboard

def confirm_keyboard(trip):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text="✅ Записаться", callback_data=f'confirm:{trip.get("title")}'))
    return keyboard