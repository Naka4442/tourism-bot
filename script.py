from telebot import TeleBot, types
from config import TOKEN
from keyboards import keyboard, trip_keyboard, confirm_keyboard, date_keyboard
from trips import TRIPS, find, info, category, index
from datetime import datetime, timedelta
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
    if message.chat.id not in users.keys():
        users[message.chat.id] = {}
    print(f"{message.from_user.first_name} ({message.chat.id}) вошел в бота")
    bot.send_message(
        message.chat.id, 
        "Привет! Это бот для записи на туристические мероприятия. Скажите, в какой поход вы хотели бы пойти?",
        reply_markup=keyboard(*COMMANDS)
    )

@bot.message_handler(content_types=["text"])
def any(message : types.Message):
    if message.chat.id not in users.keys():
        users[message.chat.id] = {}
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
    users[call.message.chat.id]["trip"] = trip
    group = f'ограничение от {trip.get("group")[0]} до {trip.get("group")[1]} чел.' if trip.get("group") else 'не ограничено'
    bot.send_message(call.message.chat.id, f"Введите пожалуйста размер группы ({group})")
    bot.register_next_step_handler(call.message, get_group_size, trip)

def get_group_size(message : types.Message, trip):
    if message.text.lower() == "отмена":
        start(message)
    size = int(message.text)
    users[message.chat.id]["size"] = size
    if not trip.get("group") or (isinstance(trip.get("group"), tuple) and size >= trip.get("group")[0] and size <= trip.get("group")[1]):
        bot.send_message(message.chat.id, "Отлично! Теперь выберите дату проведения мероприятия", reply_markup=date_keyboard())
    else:
        bot.send_message(message.chat.id, "Неподходящий размер группы, введите еще раз пожалуйста или нажмите \"отмена\"", reply_markup=keyboard("отмена"))
        bot.register_next_step_handler(message, get_group_size, trip)

@bot.callback_query_handler(func=lambda call: call.data.split(":")[0] == "date")
def get_date(call : types.CallbackQuery):
    date = datetime.now() + timedelta(days=int(call.data.split()[1]))
    users[call.message.chat.id]["date"] = date
    user = users[call.message.chat.id]
    bot.edit_message_text(f"Вы выбрали {date.strftime('%d.%m')}!", call.message.chat.id, call.message.message_id)
    cat = ["пеший", "водный", "велосипедный"][["hiking", "kayaking", "cycling"].index(category(user.get("trip")))]
    bot.send_message(call.message.chat.id, f"Вы записали {user.get('size')} чел. на {cat} поход \"{user.get('trip').get('title')}\" ({date.strftime('%d.%m')})!")


bot.infinity_polling()