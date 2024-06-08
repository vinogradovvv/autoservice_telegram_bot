"""
choosing_worker function file
"""
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler
from telegram_api.keyboards import admin_home_keyboard, skip_vin_keyboard
from database.model.model import db, OpenedWorkOrders
from database.core import db_actions

db_update = db_actions.update()


async def choosing_worker(update: Update, context: ContextTypes.DEFAULT_TYPE) -> [str, ConversationHandler.END]:
    """
    Function saves chosen worker
    :param update: incoming update
    :param context: update context
    :return: next conversation state or ConversationHandler.END
    """
    query = update.callback_query
    if context.user_data['mode'] == 'add_new_car':
        context.user_data['new_car']['worker'] = query.data
        markup = InlineKeyboardMarkup(skip_vin_keyboard)
        context.user_data['markup'] = markup
        await query.edit_message_text("Введите последние 7 символов VIN",
                                      reply_markup=markup)
        return 'INPUT_VIN'
    elif context.user_data['mode'] == 'edit_car':
        db_update(db,
                  OpenedWorkOrders,
                  context.user_data['car_id'],
                  'worker',
                  query.data)
        markup = ReplyKeyboardMarkup(admin_home_keyboard, one_time_keyboard=True)
        context.user_data['markup'] = markup
        await query.message.reply_text('Запись сохранена',
                                       reply_markup=markup)
        return ConversationHandler.END
