"""
choosing_filter function file
"""
from telegram import Update, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram_api.keyboards import products_keyboard, cancel_button


async def choosing_filter(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """
    Function asks user to input price range if 'price range' filter was chosen,
    or asks to choose the product manufacturer
    :param update: incoming update
    :param context: update context
    :return: next conversation state
    """
    query = update.callback_query
    product_filter = query.data
    if product_filter == 'price_range':
        data = context.user_data['products']
        price_min = min(next(iter(data.values()))['prices'])
        price_max = max(next(reversed(data.values()))['prices'])
        markup = InlineKeyboardMarkup([cancel_button])
        context.user_data['markup'] = markup
        await query.edit_message_text(f'Введите минмимальную и максимальную цену '
                                      f'в диапазоне от {price_min} до {price_max} через "-"',
                                      reply_markup=markup)
        return 'INPUT_PRICE'
    else:
        keyboard_data = context.user_data['products']
        context.user_data['products'] = None
        markup = InlineKeyboardMarkup(products_keyboard(keyboard_data, product_filter))
        context.user_data['markup'] = markup
        await query.edit_message_text('Выберите производителя',
                                      reply_markup=markup)
        return 'CHOOSING_PRODUCT'
