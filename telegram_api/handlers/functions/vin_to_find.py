"""
vin_to_find function file
"""
from telegram import Update, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram_api.keyboards import cancel_button


async def vin_to_find(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """
    Function asks user to input last 7 chars of cars vin code
    :param update: incoming update
    :param context: update context
    :return: next conversation state
    """
    context.user_data['mode'] = 'history_search'
    markup = InlineKeyboardMarkup([cancel_button])
    context.user_data['markup'] = markup
    await update.message.reply_text("Введите последние 7 символов VIN",
                                    reply_markup=markup)
    return 'INPUT_VIN'
