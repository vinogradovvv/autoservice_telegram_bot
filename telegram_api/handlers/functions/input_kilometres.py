"""
input_kilometres function file
"""
from telegram import Update, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram_api.keyboards import cancel_button


async def input_kilometres(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """
    Function saves kilometres in context.
    :param update: incoming update
    :param context: update context
    :return: next conversation state INPUT_WORKS
    """
    kilometres = update.message.text
    context.user_data['new_car']['kilometres'] = kilometres
    markup = InlineKeyboardMarkup([cancel_button])
    context.user_data['markup'] = markup
    await update.message.reply_text("Введите по одной требуемые работы",
                                    reply_markup=markup)
    return 'INPUT_WORKS'
