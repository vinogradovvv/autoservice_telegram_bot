"""
list_cart function file
"""
from telegram import Update, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram_api.keyboards import cart_keyboard, admins_options_keyboard
from euroauto_api.core import euroauto_api
from database.model.model import db, OpenedWorkOrders
from database.core import db_actions

db_get = db_actions.get()

check_token = euroauto_api.check_token()
list_euroauto_cart = euroauto_api.list_cart()


async def list_cart(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """
    Function get Euroauto cart through API and list it to user in reply.
    :param update: incoming update
    :param context: update context
    :return: next conversation state
    """
    query = update.callback_query
    check_token()
    try:
        cart = list_euroauto_cart()['data']
    except TypeError:
        car = db_get(db, OpenedWorkOrders, OpenedWorkOrders.id == context.user_data['car_id'])
        markup = InlineKeyboardMarkup(admins_options_keyboard(car))
        context.user_data['markup'] = markup
        await query.edit_message_text('Корзина пуста.',
                                      reply_markup=markup)
        return 'CAR_ACTIONS'
    context.user_data['cart'] = cart
    message = '\n\n'.join(
        [(
            f"{cart['manufacturer_codes'][cart['products'][item['product_id']]['manufacturer_code']]['manufacturer']['name']} "
            f"{cart['manufacturer_codes'][cart['products'][item['product_id']]['manufacturer_code']]['code']}\n"
            f"{cart['products'][item['product_id']]['name']['name']}\n"
            f"{cart['products'][item['product_id']]['comment']}")
            for item in cart['items']])
    markup = InlineKeyboardMarkup(cart_keyboard)
    context.user_data['markup'] = markup
    await query.edit_message_text(f'Содержимое корзины: \n{message}',
                                  reply_markup=markup)
    return 'LIST_CART'
