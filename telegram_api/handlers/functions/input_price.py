"""
input_price function file
"""
import re
from telegram import Update, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram_api.keyboards import products_keyboard, cancel_button


async def input_price(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """
    Function checks users price range and asks user to choose product,
    if any products with this price exists
    :param update: incoming update
    :param context: update context
    :return: next conversation state
    """
    prices_str = update.message.text
    if re.match(r'^\d+-\d+$', prices_str):
        price_min, price_max = [int(price) for price in prices_str.split('-')]
        keyboard_data = context.user_data['products']
        keyboard = products_keyboard(keyboard_data=keyboard_data,
                                     product_filter='price_range',
                                     price_min=price_min,
                                     price_max=price_max)
        if len(keyboard) > 1:
            context.user_data['products'] = None
            markup = InlineKeyboardMarkup(
                products_keyboard(keyboard_data=keyboard_data,
                                  product_filter='price_range',
                                  price_min=price_min,
                                  price_max=price_max))
            context.user_data['markup'] = markup
            await update.message.reply_text('Выберите производителя',
                                            reply_markup=markup)
            return 'CHOOSING_PRODUCT'
        else:
            data = context.user_data['products']
            price_min = min(next(iter(data.values()))['prices'])
            price_max = max(next(reversed(data.values()))['prices'])
            markup = InlineKeyboardMarkup([cancel_button])
            context.user_data['markup'] = markup
            await update.message.reply_text('В указанном диапазоне цен предложений нет.\n'
                                            'Введите минмимальную и максимальную цену в диапазоне от '
                                            f'{price_min} до {price_max} через "-"',
                                            reply_markup=markup)
            return 'INPUT_PRICE'
    else:
        data = context.user_data['products']
        price_min = min(next(iter(data.values()))['prices'])
        price_max = max(next(reversed(data.values()))['prices'])
        markup = InlineKeyboardMarkup([cancel_button])
        context.user_data['markup'] = markup
        await update.message.reply_text(f'Некоррекный ввод!!!\nВведите минмимальную и максимальную цену '
                                        f'в диапазоне от {price_min} до {price_max} через "-"',
                                        reply_markup=markup)
        return 'INPUT_PRICE'
