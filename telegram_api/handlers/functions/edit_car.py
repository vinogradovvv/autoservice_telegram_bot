"""
edit_car function file
"""
from telegram import Update, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram_api.keyboards import edit_car_keyboard
from database.core import db_actions

db_get = db_actions.get()


async def edit_car(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """
    Function asks user to choose what to edit
    :param update: incoming update
    :param context: update context
    :return: next conversation state
    """
    query = update.callback_query
    context.user_data['mode'] = 'edit_car'
    markup = InlineKeyboardMarkup(edit_car_keyboard)
    context.user_data['markup'] = markup
    await query.edit_message_text('Что изменить?',
                                  reply_markup=markup)
    return 'EDIT_CAR'
