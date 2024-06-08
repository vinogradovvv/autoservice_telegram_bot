"""
save_vin function file
"""
from telegram import Update, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram_api.keyboards import cancel_button
from database.model.model import db, OpenedWorkOrders
from database.core import db_actions

db_update = db_actions.update()


async def save_vin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """
    Function saves vin, and asks user to input car body code.
    :param update: incoming update
    :param context: update context
    :return: next conversation state
    """
    if context.user_data['mode'] == 'add_new_car':
        query = update.callback_query
        markup = InlineKeyboardMarkup([cancel_button])
        context.user_data['markup'] = markup
        await query.edit_message_text("Введите код кузова",
                                      reply_markup=markup)
        return 'INPUT_BODY_CODE'
    elif context.user_data['mode'] == 'edit_car':
        query = update.callback_query
        db_update(db,
                  OpenedWorkOrders,
                  context.user_data['car_id'],
                  'vin_code',
                  context.user_data['car_vin'])
        db_update(db,
                  OpenedWorkOrders,
                  context.user_data['car_id'],
                  'car_data',
                  context.user_data['car_data'])
        markup = InlineKeyboardMarkup([cancel_button])
        context.user_data['markup'] = markup
        await query.message.reply_text('Введите код кузова',
                                       reply_markup=markup)
        return 'INPUT_BODY_CODE'
