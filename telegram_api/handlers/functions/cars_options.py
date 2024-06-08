"""
cars_options function file
"""
import ast
from telegram import Update, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram_api.keyboards import workers_options_keyboard, admins_options_keyboard
from database.model.model import db, OpenedWorkOrders
from database.core import db_actions

db_get = db_actions.get()


async def cars_options(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """
    Function prints info about chosen car, and asks user for action
    :param update: incoming update
    :param context: update context
    :return: next conversation state
    """
    query = update.callback_query
    context.user_data['car_id'] = query.data
    car = db_get(db, OpenedWorkOrders, OpenedWorkOrders.id == query.data)
    context.user_data['car_link'] = ast.literal_eval(car.car_data)['catalog_link']
    works = ast.literal_eval(car.works)
    works.insert(0, 'Работы:')
    message_text = '\n - '.join(works)
    parts = ast.literal_eval(car.parts)
    if len(parts) > 0:
        parts_text = ['Запчасти:']
        for part in parts.values():
            parts_text.append(part)
        parts_text = '\n - '.join(parts_text)
        message_text = '\n'.join([message_text, parts_text])
    if context.user_data['group'] == 'workers':
        keyboard = workers_options_keyboard(car)
    else:
        keyboard = admins_options_keyboard(car)
    markup = InlineKeyboardMarkup(keyboard)
    context.user_data['markup'] = markup
    await query.edit_message_text(message_text,
                                  reply_markup=markup)
    return 'CAR_ACTIONS'
