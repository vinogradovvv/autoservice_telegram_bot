"""
save_parts function file
"""
from telegram import Update, InlineKeyboardMarkup
from telegram_api.keyboards import parts_keyboard
from telegram.ext import ContextTypes
from database.model.model import db, OpenedWorkOrders
from database.core import db_actions

db_update = db_actions.update()


async def save_parts(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """
    Function saves parts list of chosen car to database table
    :param update: incoming update
    :param context: update context
    :return: next conversation state
    """
    query = update.callback_query
    parts = context.user_data['car_parts']
    db_update(db, OpenedWorkOrders, context.user_data['car_id'], 'parts', parts)
    markup = InlineKeyboardMarkup(parts_keyboard(parts))
    context.user_data['markup'] = markup
    await query.edit_message_text('Выберите деталь для заказа в EuroAuto',
                                  reply_markup=markup)
    return 'CHOOSING_PART'
