"""
skip_vin function file
"""
from telegram import Update, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from bmw_decode.core import bmw_decoder
from telegram_api.keyboards import cancel_button

catalog = bmw_decoder.get_catalog()


async def skip_vin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """
    Function asks user to input car body code
    :param update: incoming update
    :param context: update context
    :return: next conversation state
    """
    query = update.callback_query
    context.user_data['new_car']['car_data'] = {}
    context.user_data['new_car']['car_data']['catalog_link'] = catalog
    markup = InlineKeyboardMarkup([cancel_button])
    context.user_data['markup'] = markup
    await query.edit_message_text("Введите код кузова",
                                  reply_markup=markup)
    return 'INPUT_BODY_CODE'
