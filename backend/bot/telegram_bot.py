import logging
import os

from telegram import Update, ForceReply
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler, ContextTypes, Application, filters
)
from dotenv import load_dotenv

from backend.app.services.springs import Springs

load_dotenv()
user_messages = []

TOKEN_BOT = os.getenv('TOKEN_BOT')

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    await update.message.reply_text(update.message.text)


async def hello(update: Update, context):
    text = 'Расчет пружин: необходимо последовательно ввести параметры'
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)


def main():
    s = Springs()
    application = Application.builder().token(TOKEN_BOT).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    application.add_handler(CommandHandler('hello', hello))
    application.run_polling()


if __name__ == '__main__':
    main()
