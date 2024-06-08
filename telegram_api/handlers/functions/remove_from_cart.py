"""
remove_from_cart function file
"""
from telegram import Update, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram_api.keyboards import cart_items_keyboard


async def remove_from_cart(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """
    Function asks user to choose the item to remove from Euroauto cart
    :param update: incoming update
    :param context: update context
    :return: next conversation state
    """
    query = update.callback_query
    cart = context.user_data['cart']
    markup = InlineKeyboardMarkup(cart_items_keyboard(cart))
    context.user_data['markup'] = markup
    await query.edit_message_text('Выберите позицию для удаления',
                                  reply_markup=markup)
    return 'REMOVE_FROM_CART'
