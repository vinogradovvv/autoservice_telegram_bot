"""
edit_vin function file
"""
from telegram import Update, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram_api.keyboards import cancel_button


async def edit_vin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """
    Function asks user to input cars vin code
    :param update: incoming update
    :param context: update context
    :return: next conversation state
    """
    query = update.callback_query
    context.user_data['mode'] = 'edit_car'
    markup = InlineKeyboardMarkup([cancel_button])
    context.user_data['markup'] = markup
    await query.edit_message_text("Введите последние 7 символов VIN",
                                  reply_markup=markup)
    return 'INPUT_VIN'
