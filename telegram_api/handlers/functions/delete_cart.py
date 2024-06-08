"""
delete_cart function file
"""
from telegram import Update, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram_api.keyboards import admins_options_keyboard
from euroauto_api.core import euroauto_api
from database.model.model import db, OpenedWorkOrders
from database.core import db_actions

db_get = db_actions.get()
check_token = euroauto_api.check_token()
delete_euroauto_cart = euroauto_api.delete_cart()


async def delete_cart(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """
    Function delete Euroauto cart
    :param update: incoming update
    :param context: update context
    :return: next conversation state
    """
    query = update.callback_query
    check_token()
    response = delete_euroauto_cart()
    car = db_get(db, OpenedWorkOrders, OpenedWorkOrders.id == context.user_data['car_id'])
    if isinstance(response, dict):
        markup = InlineKeyboardMarkup(admins_options_keyboard(car))
        context.user_data['markup'] = markup
        await query.edit_message_text('Корзина удалена.',
                                      reply_markup=markup)
        return 'CAR_ACTIONS'
