"""
choose_another_date function file
"""
from telegram import Update
from telegram.ext import ContextTypes
from telegram_api.keyboards import calendar_keyboard
from database.core import db_actions

db_read = db_actions.retrieve()


async def choose_another_date(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """
    Function clears list of cars on chosen date in context, recreates calendar keyboard,
    marks busy dates, and asks user the date when new car will come
    :param update: incoming update
    :param context: update context
    :return: next conversation state CHOOSING_DATE
    """
    query = update.callback_query
    context.user_data['cars_on_date'] = []
    markup = calendar_keyboard()
    context.user_data['markup'] = markup
    await query.edit_message_text("Когда приедет?", reply_markup=markup)
    return 'CHOOSING_DATE'
