"""
remove_item function file
"""
from telegram import Update, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram_api.keyboards import admins_options_keyboard
from euroauto_api.core import euroauto_api
from database.model.model import db, OpenedWorkOrders
from database.core import db_actions

db_get = db_actions.get()
check_token = euroauto_api.check_token()
remove_from_euroauto_cart = euroauto_api.remove_item()


async def remove_item(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """
    Function removes an item from the Euroauto cart
    :param update: incoming update
    :param context: update context
    :return: next conversation state
    """
    query = update.callback_query
    offer_id = query.data
    context.user_data['cart'] = None
    car = db_get(db, OpenedWorkOrders, OpenedWorkOrders.id == context.user_data['car_id'])
    check_token()
    response = remove_from_euroauto_cart(offer_id)
    if isinstance(response, dict):
        markup = InlineKeyboardMarkup(admins_options_keyboard(car))
        context.user_data['markup'] = markup
        await query.edit_message_text('Позиция удалена.',
                                      reply_markup=markup)
        return 'CAR_ACTIONS'
