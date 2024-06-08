"""
choosing_offer function file
"""
from telegram import Update, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram_api.keyboards import add_to_cart_keyboard
from euroauto_api.core import euroauto_api
from settings import EuroautoSettings

euroauto = EuroautoSettings()
check_token = euroauto_api.check_token()
find_offers = euroauto_api.find_offers()


async def choosing_offer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """
    Function asks user to input quantity of product if where is more than one in stock
    :param update: incoming update
    :param context: update context
    :return: next conversation state
    """
    query = update.callback_query
    offer_id, offer_quantity = query.data.split(',')
    if '-' in offer_quantity:
        offer_quantity = int(offer_quantity.replace('-', ''))
    else:
        offer_quantity = int(offer_quantity)
    context.user_data['offer_id'] = offer_id
    context.user_data['offer_quantity'] = offer_quantity
    if offer_quantity > 1:
        markup = InlineKeyboardMarkup(add_to_cart_keyboard(offer_id))
        context.user_data['markup'] = markup
        await query.edit_message_text(text=f'На складе в наличии {offer_quantity} шт.\n'
                                           f'Введите количество от 1 до {offer_quantity}',
                                      reply_markup=markup)
        return 'CHOOSING_QUANTITY'
    else:
        markup = InlineKeyboardMarkup(add_to_cart_keyboard(offer_id))
        context.user_data['markup'] = markup
        await query.edit_message_text(text=f'На складе в наличии {offer_quantity} шт.',
                                      reply_markup=markup)
        return 'ADD_TO_CART'
