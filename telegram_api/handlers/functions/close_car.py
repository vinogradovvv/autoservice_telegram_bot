"""
close_car function file
"""
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler
from telegram_api.keyboards import admin_home_keyboard
from database.model.model import db, OpenedWorkOrders, ClosedWorkOrders
from database.core import db_actions

db_move = db_actions.move()


async def close_car(update: Update, context: ContextTypes.DEFAULT_TYPE) -> ConversationHandler.END:
    """
    Function moves car from open works database table to closed
    :param update: incoming update
    :param context: update context
    :return: ConversationHandler.END
    """
    query = update.callback_query
    db_move(db,
            OpenedWorkOrders,
            ClosedWorkOrders,
            context.user_data['car_id'])
    markup = ReplyKeyboardMarkup(admin_home_keyboard, one_time_keyboard=True)
    context.user_data['markup'] = markup
    await query.message.reply_text('Запись перенесена в выполненные.',
                                   reply_markup=markup)
    return ConversationHandler.END
