import logging
import os

from telegram import Update, ForceReply, InlineKeyboardMarkup, \
    InlineKeyboardButton
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler, ContextTypes, Application, filters, CallbackQueryHandler
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
        rf"Hi {user.mention_html()}! Введите вес на переднюю ось (кг)",
        reply_markup=ForceReply(selective=True),
    )


async def hendle_message(
        update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text
    chat_id = update.message.chat_id
    responses = context.chat_data.get('responses', {})

    if 'front_axle' not in responses:
        responses['front_axle'] = float(text)
        await update.message.reply_html(
            "Вес на заднюю ось (кг):",
        )
    elif 'back_axle' not in responses:
        responses['back_axle'] = float(text)
        await update.message.reply_html(
            "Вес переднего моста (кг):",
        )
    elif 'not_sus_axle_front' not in responses:
        responses['not_sus_axle_front'] = float(text)
        await update.message.reply_html(
            "Вес заднего моста (кг):",
        )
    elif 'not_sus_axle_back' not in responses:
        responses['not_sus_axle_back'] = float(text)
        await update.message.reply_html(
            "Вес одного переднего колеса (кг):",
        )
    elif 'wheel_front' not in responses:
        responses['wheel_front'] = float(text)
        await update.message.reply_html(
            "Вес одного заднего колеса (кг):",
        )

    else:
        if 'wheel_back' not in responses:
            responses['wheel_back'] = float(text)
        keyboard = [
            [InlineKeyboardButton("Рассчитать", callback_data="calculate")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("Все сообщения получены!"
                                        " нажмите кнопку Рассчитать",
                                        reply_markup=reply_markup)

    context.chat_data['responses'] = responses


async def process_calculate(update: Update,
                            context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    if query.data == 'calculate':

        response = context.chat_data['responses']
        spring_user = Springs(**response)
        result = spring_user.get_summary_data()

        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=result
        )


def process_responses(responses) -> str:
    for key, value in responses.items():
        text = f'{key}: {value}'
        user_messages.append(text)
    return '\n'.join(user_messages)


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
    # application.add_handler(
    #     MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    application.add_handler(
        CallbackQueryHandler(process_calculate)
    )
    application.add_handler(CommandHandler('hello', hello))
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, hendle_message)
    )
    application.run_polling()


if __name__ == '__main__':
    main()
