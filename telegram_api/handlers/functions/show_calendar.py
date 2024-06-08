"""
show_calendar function file
"""
from telegram import Update
from telegram.ext import ContextTypes
from telegram_api.keyboards import calendar_keyboard
from database.core import db_actions

db_read = db_actions.retrieve()


async def show_calendar(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """
    Function shows calendar keyboard marked with busy dates, and asks user to choose the date
    :param update: incoming update
    :param context: update context
    :return: next conversation state
    """
    context.user_data['cars_on_date'] = []
    if context.user_data['group'] == 'workers':
        marked_calendar = calendar_keyboard(worker=context.user_data['role'])
    else:
        marked_calendar = calendar_keyboard()
    context.user_data['markup'] = marked_calendar
    await update.message.reply_text("Выберите дату", reply_markup=marked_calendar)
    return 'SHOW_CARS'
