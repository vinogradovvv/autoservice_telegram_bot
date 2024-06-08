"""
input_vin_again function file
"""
from telegram import Update, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram_api.keyboards import cancel_button


async def input_vin_again(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """
    Function allows user to reenter VIN code if function button was pressed.
    :param update: incoming update
    :param context: update context
    :return: INPUT_VIN state
    """
    query = update.callback_query
    markup = InlineKeyboardMarkup([cancel_button])
    context.user_data['markup'] = markup
    await query.edit_message_text("Введите последние 7 символов VIN",
                                  reply_markup=markup)
    return 'INPUT_VIN'
