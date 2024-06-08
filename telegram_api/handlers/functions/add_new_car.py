"""
add_new_car function file
"""
from telegram import Update
from telegram.ext import ContextTypes
from telegram_api.keyboards import calendar_keyboard
from database.core import db_actions

db_read = db_actions.retrieve()


async def add_new_car(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """
    Function creates lists and dicts in context to store data, creates calendar keyboard,
    marks when records exist, and asks user of date new car will come
    :param update: incoming update
    :param context: update context
    :return: next conversation state CHOOSING_DATE
    """
    context.user_data['mode'] = 'add_new_car'
    context.user_data['new_car'] = {}
    context.user_data['new_car']['parts'] = {}
    context.user_data['new_car']['works'] = []
    context.user_data['new_car']['comment'] = []
    marked_calendar = calendar_keyboard()
    context.user_data['markup'] = marked_calendar
    await update.message.reply_text("Когда приедет?", reply_markup=marked_calendar)
    return 'CHOOSING_DATE'
