"""
edit_arrive function file
"""
from telegram import Update
from telegram.ext import ContextTypes
from telegram_api.keyboards import calendar_keyboard


async def edit_arrive_datetime(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """
    Function asks user to choose arrive date
    :param update: incoming update
    :param context: update context
    :return: next conversation state
    """
    query = update.callback_query
    markup = calendar_keyboard()
    context.user_data['markup'] = markup
    await query.edit_message_text("Выберите дату", reply_markup=markup)
    return 'CHOOSING_DATE'
