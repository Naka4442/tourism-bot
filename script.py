from telebot import TeleBot
from config import TOKEN
from keyboards import keyboard


bot = TeleBot(TOKEN)

@bot.message_handler(commands=["start"])
def start(message):
    print(f"{message.from_user.first_name} вошел в бота")
    bot.send_message(
        message.chat.id, 
        "Привет! Это бот для записи на туристические мероприятия. Скажите, в какой поход вы хотели бы пойти?",
        reply_markup=keyboard("🚶‍♂️ Пеший", "⛵️ Водный", "🚴‍♂️ Велосипедный")
    )


bot.infinity_polling()