"""
confirm_time function file
"""
from telegram import Update, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler
from telegram_api.keyboards import workers_keyboard, choose_another_time_keyboard, admin_home_keyboard
from telegram_api.handlers.functions.keyboard_marker import mark_workers
from database.model.model import db, OpenedWorkOrders
from database.core import db_actions

db_update = db_actions.update()


async def confirm_time(update: Update, context: ContextTypes.DEFAULT_TYPE) -> [str, ConversationHandler.END]:
    """
    Function creates workers keyboard, depends of busy worker this time, or not.
    If all workers are busy this time function asks to choose another time.
    :param update: incoming update
    :param context: update context
    :return: next conversation state CHOOSING_WORKER or CONFIRMING_TIME
    """
    query = update.callback_query
    busy_workers = [car.worker for car in context.user_data['cars_on_time']]
    if context.user_data['mode'] == 'add_new_car':
        if len(busy_workers) == 0:
            keyboard = workers_keyboard()
        else:
            keyboard = mark_workers(workers_keyboard(), busy_workers)
        if len(keyboard) > 0:
            markup = InlineKeyboardMarkup(keyboard)
            context.user_data['markup'] = markup
            await query.edit_message_text("Назначте исполнителя",
                                          reply_markup=markup)
            return 'CHOOSING_WORKER'
        else:
            markup = InlineKeyboardMarkup(choose_another_time_keyboard)
            context.user_data['markup'] = markup
            await query.edit_message_text("В выбранное время все работники заняты!",
                                          reply_markup=markup)
            return 'CONFIRMING_TIME'
    elif context.user_data['mode'] == 'edit_car':
        if context.user_data['role'] in busy_workers:
            markup = InlineKeyboardMarkup(choose_another_time_keyboard)
            context.user_data['markup'] = markup
            await query.edit_message_text(f"В выбранное время {context.user_data['role']} занят!",
                                          reply_markup=markup)
            return 'CONFIRMING_TIME'
        else:
            db_update(db,
                      OpenedWorkOrders,
                      context.user_data['car_id'],
                      'arrive_datetime',
                      context.user_data['car_arrive'])
            context.user_data['cars_on_date'] = []
            context.user_data['cars_on_time'] = []
            context.user_data['car_id'] = None
            context.user_data['car_arrive'] = None
            markup = ReplyKeyboardMarkup(admin_home_keyboard, one_time_keyboard=True)
            context.user_data['markup'] = markup
            await query.message.reply_text('Запись сохранена',
                                           reply_markup=markup)
            return ConversationHandler.END
