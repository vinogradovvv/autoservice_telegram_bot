"""
edit_worker function file
"""
from telegram import Update, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler
from telegram_api.keyboards import workers_keyboard, admin_home_keyboard
from telegram_api.handlers.functions.keyboard_marker import mark_workers
from database.model.model import db, OpenedWorkOrders
from database.core import db_actions

db_read = db_actions.retrieve()
db_get = db_actions.get()


async def edit_worker(update: Update, context: ContextTypes.DEFAULT_TYPE) -> [str, ConversationHandler.END]:
    """
    Function asks user to choose the worker if anyone is free at this time
    :param update: incoming update
    :param context: update context
    :return: next conversation state or ConversationHandler.END
    """
    query = update.callback_query
    car = db_get(db, OpenedWorkOrders, OpenedWorkOrders.id == context.user_data['car_id'])
    cars_on_time = db_read(db, OpenedWorkOrders).where(OpenedWorkOrders.arrive_datetime == car.arrive_datetime)
    busy_workers = [car.worker for car in cars_on_time]
    keyboard = mark_workers(workers_keyboard(), busy_workers)
    if len(keyboard) > 0:
        markup = InlineKeyboardMarkup(keyboard)
        context.user_data['markup'] = markup
        await query.edit_message_text("Назначте исполнителя",
                                      reply_markup=markup)
        return 'CHOOSING_WORKER'
    else:
        markup = ReplyKeyboardMarkup(admin_home_keyboard, one_time_keyboard=True)
        context.user_data['markup'] = markup
        await update.message.reply_text("В выбранное время все остальные работники заняты!\n"
                                        "Измените дату/время приезда если переназначить исполнителя необходимо.",
                                        reply_markup=markup)
        return ConversationHandler.END
