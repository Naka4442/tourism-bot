from telebot import TeleBot, types
from config import TOKEN
from keyboards import keyboard, trip_keyboard, confirm_keyboard
from trips import TRIPS, find, info, category, index
import os


COMMANDS = [
    "🚶‍♂️ Пеший",
    "⛵️ Водный",
    "🚴‍♂️ Велосипедный"
]

users = dict()

bot = TeleBot(TOKEN)

@bot.message_handler(commands=["start"])
def start(message : types.Message):
    print(f"{message.from_user.first_name} ({message.chat.id}) вошел в бота")
    bot.send_message(
        message.chat.id, 
        "Привет! Это бот для записи на туристические мероприятия. Скажите, в какой поход вы хотели бы пойти?",
        reply_markup=keyboard(*COMMANDS)
    )

@bot.message_handler(content_types=["text"])
def any(message : types.Message):
    if message.chat.id not in users.keys():
        if message.text not in COMMANDS:
            bot.send_message(
                message.chat.id,
                text="Не знаю такой команды. Скажите, в какой поход вы хотели бы пойти?",
                reply_markup=keyboard(*COMMANDS)
            )
        else:
            if message.text == COMMANDS[0]:
                bot.send_message(
                    message.chat.id,
                    text="🚶‍♂️ Пешие походы",
                    reply_markup=trip_keyboard(*TRIPS["hiking"])
                )
            elif message.text == COMMANDS[1]:
                bot.send_message(
                    message.chat.id,
                    text="⛵️ Водные походы",
                    reply_markup=trip_keyboard(*TRIPS["kayaking"])
                )
            elif message.text == COMMANDS[2]:
                bot.send_message(
                    message.chat.id,
                    text="🚴‍♂️ Велосипедные походы",
                    reply_markup=trip_keyboard(*TRIPS["cycling"])
                )

@bot.callback_query_handler(func=lambda call: call.data.split(":")[0] == "trip")
def callback_trip(call : types.CallbackQuery):
    title = call.data.split(":")[1]
    trip = find(title)
    bot.edit_message_text(title, call.message.chat.id, call.message.message_id, parse_mode="html")
    for i in range(1, 3):
        with open(f"images/{category(trip)}/{index(trip) + 1}/{i}.jpg", "rb") as file:
            bot.send_photo(call.message.chat.id, file)
    bot.send_message(call.message.chat.id, info(trip), parse_mode="html", reply_markup=confirm_keyboard(trip))


@bot.callback_query_handler(func=lambda call: call.data.split(":")[0] == "confirm")
def confirm_trip(call : types.CallbackQuery):
    title = call.data.split(":")[1]
    trip = find(title)
    group = {f'от {trip.get("group")[0]} до {trip.get("group")[1]} чел.' if trip.get("group") else 'не ограничено'}
    bot.send_message(call.message.chat.id, f"Введите пожалуйста размер группы (ограничение {group})")
    bot.register_next_step_handler(call.message, get_group_size, trip)

def get_group_size(message : types.Message, trip):
    size = int(message.text)
    if not trip.get("group") or (isinstance(trip.get("group"), tuple) and size >= trip.get("group")[0] and size <= trip.get("group")[1]):
        bot.send_message(message.chat.id, "Отлично! Теперь выберите дату проведения мероприятия")
    else:
        bot.send_message(message.chat.id, "Неподходящий размер группы, введите еще раз пожалуйста или нажмите \"отмена\"")
        bot.register_next_step_handler(message, get_group_size)


bot.infinity_polling()