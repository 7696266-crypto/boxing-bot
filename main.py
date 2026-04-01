import telebot
import os

TOKEN = os.getenv("TOKEN") or "8525030646:AAGGM022Ih-5XZzu7585t33QnIoO2bRmct0"
ADMIN_ID = int(os.getenv("ADMIN_ID") or "7188013735")

bot = telebot.TeleBot(TOKEN)

user_data = {}

@bot.message_handler(commands=['start'])
def start(message):
    print(message.text)
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("Course", "Contact")

    bot.send_message(
        message.chat.id,
        "🥊 Welcome to Almaskhan Boxing System\n\n"
        "If you are a beginner and do not know where to start, this course is for you.\n\n"
        "Learn boxing step by step:\n"
        "• stance\n"
        "• punches\n"
        "• footwork\n"
        "• defense\n"
        "• beginner combinations\n\n"
        "Choose an option below 👇",
        reply_markup=markup
    )
    

@bot.message_handler(func=lambda message: message.text == "Course")
def course(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("💳 Buy Access", "📚 My Lessons", "⬅️ Back")
    bot.send_message(message.chat.id, "Choose an action:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "Buy Access")
def buy(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("📩 Send Receipt")

    bot.send_message(
        message.chat.id,
        "💳 Payment Instructions\n\n" "Price: $49.90\n\n" "After payment, click the button below 👇",
        reply_markup=markup
    )

@bot.message_handler(func=lambda message: message.text == "Send Receipt")
def send_check(message):
    bot.send_message(message.chat.id, "Отправьте чек (фото или скрин)")
    bot.register_next_step_handler(message, process_check)

def process_check(message):
    bot.forward_message(ADMIN_ID, message.chat.id, message.message_id)
    bot.send_message(message.chat.id, "Чек отправлен на проверку ✅")

@bot.message_handler(commands=['approve'])
def approve(message):
    if message.chat.id == ADMIN_ID:
        try:
            user_id = int(message.text.split()[1])

            markup = telebot.types.InlineKeyboardMarkup()
            markup.add(telebot.types.InlineKeyboardButton(
                "👉 Join Private Channel",
                url="https://t.me/your_channel"
            ))

            bot.send_message(
                user_id,
                "🥊 Thank you for joining\n\n"
                "The Beginner Boxing System is currently in production.\n\n"
                "You will get full access very soon.\n\n"
                "Stay tuned 👇",
                reply_markup=markup
            )

            bot.send_message(user_id, "What do you struggle with in boxing?")
            bot.register_next_step_handler_by_chat_id(user_id, ask_email)

        except:
            bot.send_message(message.chat.id, "Ошибка")

def ask_email(message):
    user_data[message.chat.id] = {"problem": message.text}
    bot.send_message(message.chat.id, "Your email:")
    bot.register_next_step_handler(message, ask_phone)

def ask_phone(message):
    user_data[message.chat.id]["email"] = message.text
    bot.send_message(message.chat.id, "Your phone (optional):")
    bot.register_next_step_handler(message, finish)

def finish(message):
    user_data[message.chat.id]["phone"] = message.text

    data = user_data[message.chat.id]

    bot.send_message(
        ADMIN_ID,
        f"Новый пользователь:\n\n"
        f"Проблема: {data['problem']}\n"
        f"Email: {data['email']}\n"
        f"Телефон: {data['phone']}"
    )

    bot.send_message(message.chat.id, "Спасибо! Данные сохранены ✅")

bot.infinity_polling()
