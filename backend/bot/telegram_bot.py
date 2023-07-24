import os

from telegram import (
    Update, InlineKeyboardMarkup,
    InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
)
from telegram.ext import (
    CommandHandler,
    MessageHandler, ContextTypes, Application, filters, CallbackQueryHandler
)
from dotenv import load_dotenv

from backend.app.services.springs import Springs
from backend.bot.logger import logger

load_dotenv()

TOKEN_BOT = os.getenv('TOKEN_BOT')


class AllExceptions(Exception):
    pass


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    messages = (f"Привет {user.mention_html()}\n"
                "Я помогу рассчитать пружины.\n"
                "Необходимо последовательно ввести 10 параметров машины\n"

                "Вес на переднюю ось (кг):\n"
                "Вес на заднюю ось (кг):\n"
                "Вес переднего моста (кг):\n"
                "Вес заднего моста (кг):\n"
                "Вес одного переднего колеса (кг):\n"
                "Вес одного заднего колеса (кг):\n"
                "Ход передней стойки (мм):\n"
                "Ход задней стойки (мм):\n"
                "Осадка перед (%):\n"
                "Осадка зад (%):\n"
                "\n"
                "При ошибке ввода или чтобы начать заново отправьте /restart\n"
                "\n"
                "Для начала Введите Вес на переднюю ось (кг):\n"
                )

    reply_keyboard = [
        [KeyboardButton('/restart')]
    ]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True,
                                 resize_keyboard=True, )
    await update.message.reply_html(messages,
                                    reply_markup=markup,
                                    )


async def handle_restart(update: Update,
                         context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /restart."""

    context.chat_data.clear()
    await start(update, context)


async def hendle_message(
        update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Последовательно принимает сообщения и заносит их в словарь."""

    text = update.message.text
    chat_id = update.message.chat_id
    responses = context.chat_data.get('responses', {})

    if text.isdigit():
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
        elif 'wheel_back' not in responses:
            responses['wheel_back'] = float(text)
            await update.message.reply_html(
                "Ход передней стойки (мм):",
            )
        elif 'spring_stroke_front' not in responses:
            responses['spring_stroke_front'] = float(text)
            await update.message.reply_html(
                "Ход задней стойки (мм):",
            )
        elif 'spring_stroke_back' not in responses:
            responses['spring_stroke_back'] = float(text)
            await update.message.reply_html(
                "Осадка перед (%):",
            )
        elif 'draught_in_percent_front' not in responses:
            responses['draught_in_percent_front'] = float(text)
            await update.message.reply_html(
                "Осадка зад (%):",
            )

        else:
            if 'draught_in_percent_back' not in responses:
                responses['draught_in_percent_back'] = float(text)
            keyboard = [
                [InlineKeyboardButton("Рассчитать", callback_data="calculate")],
                [InlineKeyboardButton("Подробно", callback_data="more")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            resp_inter = process_responses_finished(responses)
            text = (
                    "Ведены Параметры: \n" + resp_inter + "\n" +
                    "Все сообщения получены! нажмите кнопку Рассчитать"
            )

            await update.message.reply_text(text=text,
                                            reply_markup=reply_markup)
    else:
        await update.message.reply_html(
            "Нужно ввести число!",
        )

    context.chat_data['responses'] = responses


async def process_calculate(update: Update,
                            context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обрабатывает кнопку "Рассчитать"."""

    query = update.callback_query
    try:
        logger.info(f'{query.data}, {context.chat_data}')
        if query.data == 'calculate':
            response = context.chat_data['responses']
            spring_user = Springs(**response)
            result = spring_user.get_summary_data()

            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=process_responses(result)
            )
        elif query.data == 'more':
            result = ''
            query = None

            await process_more(update, context)
    except ZeroDivisionError as e:
        logger.error(e)
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Ошибка! Введены неверные параметры! Начните заново /restart",
        )
    except AllExceptions as e:
        logger.error(e)
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Непредвиденная Ошибка! Начните заново /restart",
        )


async def process_more(update: Update,
                       context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обрабатывает кнопку "Подробно"."""

    query = update.callback_query

    try:
        logger.info(f'{query.data}, {context.chat_data}')
        if query.data == 'more':
            response = context.chat_data['responses']
            spring_user = Springs(**response)
            result = spring_user.get_calculation_of_spring_stiffness()

            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=process_responses_more(result)
            )
    except ZeroDivisionError as e:
        logger.error(e)
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Ошибка! Введены неверные параметры! Начните заново /restart",
        )
    except AllExceptions as e:
        logger.error(e)
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Непредвиденная Ошибка! Начните заново /restart",
        )


def process_responses(responses) -> str:
    """Преобразует словарь в строку."""

    user_messages = []
    for key, value in responses.items():
        text = f'{key}: {value}'
        user_messages.append(text)
    return '\n'.join(user_messages)


def process_responses_finished(responses) -> str:
    """Преобразует словарь в строку после введения всех параметров."""

    par = [
        "Вес на переднюю ось (кг):",
        "Вес на заднюю ось (кг):",
        "Вес переднего моста (кг):",
        "Вес заднего моста (кг):",
        "Вес одного переднего колеса (кг):",
        "Вес одного заднего колеса (кг):",
        "Ход передней стойки (мм):",
        "Ход задней стойки (мм):",
        "Осадка перед (%):",
        "Осадка зад (%):"
    ]
    user_messages = []
    for key, value in zip(par, responses.values()):
        text = f'{key}: {value}'
        user_messages.append(text)
    return '\n'.join(user_messages)


def process_responses_more(responses) -> str:
    """Преобразует словарь в строку по кнопке Подробно."""

    user_messages = []
    for key, value in responses.items():
        header = f'{key}:\n'
        user_messages.append(header)
        for k, v in value.items():
            hed = f'\t{k}:\n'
            user_messages.append(hed)
            for i, j in v.items():
                text = f'\t\t{i}: {j}\n'
                user_messages.append(text)

    return ''.join(user_messages)


def main():
    application = Application.builder().token(TOKEN_BOT).build()
    application.add_handler(CommandHandler('start', start))

    application.add_handler(CommandHandler('restart', handle_restart))

    application.add_handler(
        CallbackQueryHandler(process_calculate),

    )
    application.add_handler(
        CallbackQueryHandler(process_more)
    )
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, hendle_message)
    )

    application.run_polling()


if __name__ == '__main__':
    main()
