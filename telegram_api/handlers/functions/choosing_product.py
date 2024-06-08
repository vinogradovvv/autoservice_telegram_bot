"""
choosing_product function file
"""
from telegram import Update, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram_api.keyboards import offers_keyboard
from euroauto_api.core import euroauto_api
from settings import EuroautoSettings

euroauto = EuroautoSettings()
check_token = euroauto_api.check_token()
find_offers = euroauto_api.find_offers()


async def choosing_product(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """
    Function shows image of chosen product (if exists)
    and asks user to choose warehouse to order from
    :param update: incoming update
    :param context: update context
    :return: next conversation state
    """
    query = update.callback_query
    product_code = query.data
    code = product_code[4:-2]
    check_token()
    offers = find_offers(product_code)
    try:
        image = offers['data']['manufacturer_codes'][code]['media']['images'][0]['url']
    except KeyError:
        image = None
    keyboard_data = []
    for offer in offers['data']['offers']:
        if offer['id'].split('-')[1] in euroauto.stores and offer['id'].split('-')[4] == '1':
            keyboard_data.append({
                'id': offer['id'],
                'store': offers['data']['stores'][offer['store_id']]['name'],
                'quantity': offer['quantity'],
                'price': offer['price']
            })
            if offer['id'].split('-')[1] in euroauto.my_stores.split(', '):
                keyboard_data[-1]['quantity'] = f'-{keyboard_data[-1]["quantity"]}-'
    if image:
        message = f'{image}\nВыберите склад'
    else:
        message = 'Выберите склад'
    markup = InlineKeyboardMarkup(offers_keyboard(keyboard_data))
    context.user_data['markup'] = markup
    await query.edit_message_text(message,
                                  reply_markup=markup)
    return 'CHOOSING_OFFER'
