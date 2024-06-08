"""
order_parts function file
"""
from telegram import Update, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram_api.keyboards import cancel_button, save_parts_keyboard
from database.model.model import db, OpenedWorkOrders
from database.core import db_actions
import ast

db_get = db_actions.get()


async def order_parts(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """
    Function asks user to choose part from catalog and input partnumber as answer
    :param update: incoming update
    :param context: update context
    :return: next conversation state
    """
    query = update.callback_query
    car = db_get(db, OpenedWorkOrders, OpenedWorkOrders.id == context.user_data['car_id'])
    parts = ast.literal_eval(car.parts)
    link = context.user_data['car_link']
    if len(parts) == 0:
        context.user_data['car_parts'] = {}
        markup = InlineKeyboardMarkup([cancel_button])
        context.user_data['markup'] = markup
        await query.edit_message_text(f'Чтобы добавить деталь скопируйте номер из каталога'
                                      f' и отправьте в ответ\n{link}',
                                      disable_web_page_preview=True,
                                      reply_markup=markup)
    else:
        context.user_data['car_parts'] = parts
        parts_list = [f'{number} - {name}' for number, name in context.user_data['car_parts'].items()]
        parts_list_text = '\n'.join(parts_list)
        markup = InlineKeyboardMarkup(save_parts_keyboard)
        context.user_data['markup'] = markup
        await query.edit_message_text(f'{parts_list_text}\n\n'
                                      f'Чтобы добавить ещё деталь скопируйте номер из каталога'
                                      f' и отправьте в ответ\n{link}',
                                      disable_web_page_preview=True,
                                      reply_markup=markup)
    return 'INPUT_PARTS'
