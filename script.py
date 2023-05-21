from telebot import TeleBot, types
from config import TOKEN
from keyboards import keyboard


COMMANDS = [
    "🚶‍♂️ Пеший",
    "⛵️ Водный",
    "🚴‍♂️ Велосипедный"
]
bot = TeleBot(TOKEN)

@bot.message_handler(commands=["start"])
def start(message):
    print(f"{message.from_user.first_name} вошел в бота")
    bot.send_message(
        message.chat.id, 
        "Привет! Это бот для записи на туристические мероприятия. Скажите, в какой поход вы хотели бы пойти?",
        reply_markup=keyboard("🚶‍♂️ Пеший", "⛵️ Водный", "🚴‍♂️ Велосипедный")
    )

@bot.message_handler(content_types=["text"])
def any(message : types.Message):
    if message.text not in COMMANDS:
        bot.send_message(
            message.chat.id,
            text="Я тебя не понимаю, брат🤣"
        )
    else:
        if message.text == COMMANDS[0]:
            bot.send_message(
                message.chat.id,
                text="Выберите регион похода",
                reply_markup=keyboard("Ивановский", "Шуйский", "Тейковский", "Юрьевецкий", "Плесский", "Палехский", "Вичужский")
            )
        elif message.text == COMMANDS[1]:
            bot.send_message(
                message.chat.id,
                text="Выберите реку",
                reply_markup=keyboard("Уводь", "Теза", "Волга", "Клязьма", "Шуя", "Нерль", "Лух")
            )

bot.infinity_polling()