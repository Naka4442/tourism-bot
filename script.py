from telebot import TeleBot, types
from config import TOKEN
from keyboards import keyboard, trip_keyboard
from trips import TRIPS, find, info


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
    bot.edit_message_text(info(trip), call.message.chat.id, call.message.message_id, parse_mode="html")


bot.infinity_polling()