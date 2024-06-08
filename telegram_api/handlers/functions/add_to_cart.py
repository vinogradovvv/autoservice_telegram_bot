"""
add_to_cart function file
"""
from telegram import Update, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram_api.keyboards import admins_options_keyboard
from euroauto_api.core import euroauto_api
from database.model.model import db, OpenedWorkOrders
from database.core import db_actions


db_get = db_actions.get()
check_token = euroauto_api.check_token()
add_to_euroauto_cart = euroauto_api.add_to_cart()


async def add_to_cart(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """
    Function adds to euroauto cart product from given offer of given quantity with api request
    :param update: incoming update
    :param context: update context
    :return: next conversation state
    """
    query = update.callback_query
    offer_id, quantity = update.callback_query.data.split(', ')
    quantity = int(quantity)
    check_token()
    response = add_to_euroauto_cart(offer_id, quantity)
    if isinstance(response, dict):
        context.user_data['offer_id'] = None
        context.user_data['offer_quantity'] = None
        car = db_get(db, OpenedWorkOrders, OpenedWorkOrders.id == context.user_data['car_id'])
        markup = InlineKeyboardMarkup(admins_options_keyboard(car))
        context.user_data['markup'] = markup
        await query.message.reply_text('Позиция добавлена в корзину.',
                                       reply_markup=markup)
        return 'CAR_ACTIONS'
