"""
delete_car function file
"""
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler
from telegram_api.keyboards import admin_home_keyboard
from database.model.model import db, OpenedWorkOrders
from database.core import db_actions

db_delete = db_actions.remove()


async def delete_car(update: Update, context: ContextTypes.DEFAULT_TYPE) -> ConversationHandler.END:
    """
    Function delete chosen car from database table
    :param update: incoming update
    :param context: update context
    :return: ConversationHandler.END
    """
    query = update.callback_query
    db_delete(db, OpenedWorkOrders, context.user_data['car_id'])
    markup = ReplyKeyboardMarkup(admin_home_keyboard, one_time_keyboard=True)
    context.user_data['markup'] = markup
    await query.message.reply_text('Запись удалена',
                                   reply_markup=markup)
    return ConversationHandler.END
