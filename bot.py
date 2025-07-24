import google.generativeai as genai
from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, filters, ContextTypes

# === ВСТАВЬ СЮДА СВОЙ КЛЮЧИ ===
TELEGRAM_TOKEN = 'А здесь ставляите токен теелеграм бота'
GEMINI_API_KEY = 'Здсь ставляите айпи ключь ии'

# === НАСТРОЙКА GEMINI ===
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('models/gemini-2.0-flash') #это модель. можите заменить его на чего угодно 

# === Лимит токенов и хранилище пользователей ===
TOKEN_LIMIT = 15 #это лиминит тоесть токен. этот модел ии миеит 10 милеонов токенов 
user_tokens = {}

# === КОМАНДА /start ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я бот с ИИ Gemini. Напиши что угодно!")

# === ОБРАБОТКА СООБЩЕНИЙ ===
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    tokens_used = user_tokens.get(user_id, 0)
    if tokens_used >= TOKEN_LIMIT:
        await update.message.reply_text("❌ Лимит токенов (15) исчерпан.")  #это когда токен закончился. собшает ползвителтию
        return

    user_message = update.message.text
    await update.message.chat.send_action(action="typing")
    try:
        response = model.generate_content(user_message)
        reply = response.text
        await update.message.reply_text(reply)
        user_tokens[user_id] = tokens_used + 1  # Увеличиваем счётчик
    except Exception as e:
        await update.message.reply_text(f"Ошибка: {e}")

# === ЗАПУСК БОТА ===
app = Application.builder().token(TELEGRAM_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
app.run_polling()

#короче код можно поменять. но укажите имя автора HexHamder. 