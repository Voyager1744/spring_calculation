from telegram import Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler, ContextTypes
)

from backend.app.services.springs import Springs

user_messages = []


def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = 'Расчет пружин: необходимо последовательно ввести параметры'
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)


