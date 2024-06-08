"""
choosing_quantity function file
"""
from telegram import Update, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram_api.keyboards import add_to_cart_keyboard


async def choosing_quantity(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """
    Function asks user to input quantity of product to order and checks input
    :param update: incoming update
    :param context: update context
    :return: next conversation state
    """
    offer_id = context.user_data['offer_id']
    try:
        quantity = int(update.message.text)
        if 1 <= quantity <= context.user_data['offer_quantity']:
            markup = InlineKeyboardMarkup(add_to_cart_keyboard(offer_id, quantity))
            context.user_data['markup'] = markup
            await update.message.reply_text(text='Нажмите на кнопку, чтобы добавить в корзину',
                                            reply_markup=markup)
            return 'ADD_TO_CART'
        else:
            markup = InlineKeyboardMarkup(add_to_cart_keyboard(offer_id))
            context.user_data['markup'] = markup
            await update.message.reply_text(text=f'Некорректный ввод: {update.message.text}. '
                                                 f'Введите количество от 1 до {context.user_data["offer_quantity"]}.',
                                            reply_markup=markup)
            return 'CHOOSING_QUANTITY'
    except ValueError:
        markup = InlineKeyboardMarkup(add_to_cart_keyboard(offer_id))
        context.user_data['markup'] = markup
        await update.message.reply_text(text=f'Некорректный ввод: {update.message.text}. '
                                             f'Введите количество от 1 до {context.user_data["offer_quantity"]}.',
                                        reply_markup=markup)
        return 'CHOOSING_QUANTITY'
