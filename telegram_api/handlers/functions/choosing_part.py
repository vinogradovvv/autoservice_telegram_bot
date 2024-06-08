"""
choosing_part function file
"""
from telegram import Update, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram_api.keyboards import filters_keyboard
from euroauto_api.core import euroauto_api

check_token = euroauto_api.check_token()
find_products = euroauto_api.find_products()


async def choosing_part(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """
    Function asks user to choose search filter
    :param update: incoming update
    :param context: update context
    :return: next conversation state
    """
    query = update.callback_query
    part_number = query.data
    check_token()
    products = find_products(part_number)
    keyboard_data = {}
    for code, code_data in products['data']['manufacturer_codes'].items():
        name = code_data["manufacturer"]["name"]
        prices = set([offer['price'] for offer in products['data']['offers'] if code in offer["id"]])
        product_id = f'0-0-{code}-0'
        keyboard_data[name] = {'code': code,
                               'prices': prices,
                               'product_id': product_id}
    keyboard_data_sorted = {k: v for k, v in sorted(keyboard_data.items(),
                                                    key=lambda item: sorted(item[1]['prices']))}
    context.user_data['products'] = keyboard_data_sorted
    markup = InlineKeyboardMarkup(filters_keyboard)
    context.user_data['markup'] = markup
    await query.edit_message_text('Выберите фильтр поиска',
                                  reply_markup=markup)
    return 'CHOOSING_FILTER'
