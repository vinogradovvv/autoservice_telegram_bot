"""
input_body_code function file
"""
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler
from telegram_api.keyboards import admin_home_keyboard, cancel_button
from database.model.model import db, OpenedWorkOrders
from database.core import db_actions

db_update = db_actions.update()


async def input_body_code(update: Update, context: ContextTypes.DEFAULT_TYPE) -> [str, ConversationHandler.END]:
    """
    Function stores car body code and asks user to input kilometres
    :param update: incoming update
    :param context: update context
    :return: next conversation state or ConversationHandler.END
    """
    body_code = update.message.text
    if context.user_data['mode'] == 'add_new_car':
        context.user_data['new_car']['car_data']['body_code'] = body_code
        markup = InlineKeyboardMarkup([cancel_button])
        context.user_data['markup'] = markup
        await update.message.reply_text("Введите пробег",
                                        reply_markup=markup)
        return 'INPUT_KILOMETRES'
    elif context.user_data['mode'] == 'edit_car':
        context.user_data['car_data']['body_code'] = body_code
        db_update(db,
                  OpenedWorkOrders,
                  context.user_data['car_id'],
                  'car_data',
                  context.user_data['car_data'])
        markup = ReplyKeyboardMarkup(admin_home_keyboard, one_time_keyboard=True)
        context.user_data['markup'] = markup
        await update.message.reply_text('Запись сохранена',
                                        reply_markup=markup)
        return ConversationHandler.END
