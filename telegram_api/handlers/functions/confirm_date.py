"""
confirm_date function file
"""
from telegram import Update, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram_api.keyboards import time_keyboard
from telegram_api.handlers.functions.keyboard_marker import mark_times


async def confirm_date(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """
    Function saves choosen date to context, creates time keyboard, marks it with busy times,
    and asks user for time when car will come.
    :param update: incoming update
    :param context: update context
    :return: next conversation state CHOOSING_TIME
    """
    query = update.callback_query
    cars_on_date = context.user_data['cars_on_date']
    cars_times = [car.arrive_datetime.strftime('%H:%M') for car in cars_on_date]
    marked_time_keyboard = mark_times(time_keyboard(), cars_times)
    markup = InlineKeyboardMarkup(marked_time_keyboard)
    context.user_data['markup'] = markup
    await query.edit_message_text("Во сколько?",
                                  reply_markup=markup)
    return 'CHOOSING_TIME'
