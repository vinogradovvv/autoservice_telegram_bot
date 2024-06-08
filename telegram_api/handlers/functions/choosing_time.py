"""
choosing_time function file
"""
import ast
from telegram import Update, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler
from telegram_api.keyboards import workers_keyboard, confirm_time_keyboard, admin_home_keyboard
from datetime import datetime
from database.model.model import db, OpenedWorkOrders
from database.core import db_actions

db_read = db_actions.retrieve()
db_update = db_actions.update()


async def choosing_time(update: Update, context: ContextTypes.DEFAULT_TYPE) -> [str, ConversationHandler.END]:
    """
    Function process button pressing, and if time of pressed button is free
    saves time to context and returns CHOOSING_WORKER state. If chosen time is busy
    tels user about it and returns CONFIRMING_TIME state.
    :param update: incoming update
    :param context: update context
    :return: next conversation state or ConversationHandler.END
    """
    query = update.callback_query
    if len(query.data) == 5:
        arrive_time = datetime.strptime(query.data, '%H:%M').time()
        if context.user_data['mode'] == 'add_new_car':
            arrive_date = context.user_data['new_car']['arrive_datetime']
            context.user_data['new_car']['arrive_datetime'] = datetime.combine(arrive_date, arrive_time)
            context.user_data['cars_on_date'] = []
            markup = InlineKeyboardMarkup(workers_keyboard())
            context.user_data['markup'] = markup
            await query.edit_message_text("Назначте исполнителя",
                                          reply_markup=markup)
            return 'CHOOSING_WORKER'
        elif context.user_data['mode'] == 'edit_car':
            arrive_date = context.user_data['car_arrive']
            context.user_data['car_arrive'] = datetime.combine(arrive_date, arrive_time)
            context.user_data['cars_on_date'] = []
            db_update(db,
                      OpenedWorkOrders,
                      context.user_data['car_id'],
                      'arrive_datetime',
                      context.user_data['car_arrive'])
            markup = ReplyKeyboardMarkup(admin_home_keyboard,
                                         one_time_keyboard=True)
            context.user_data['markup'] = markup
            await query.message.reply_text('Запись сохранена',
                                           reply_markup=markup)
            return ConversationHandler.END
    else:
        query_time = datetime.strptime(query.data.replace('-', ''), '%H:%M').time()
        if context.user_data['mode'] == 'add_new_car':
            date = datetime.combine(context.user_data['new_car']['arrive_datetime'], query_time)
            context.user_data['new_car']['arrive_datetime'] = date
        else:
            date = datetime.combine(context.user_data['car_arrive'], query_time)
            context.user_data['car_arrive'] = date
        cars_on_time = db_read(db, OpenedWorkOrders).where(
            OpenedWorkOrders.arrive_datetime == date
        )
        context.user_data['cars_on_time'] = cars_on_time
        cars = [f"{car.worker} "
                f"{car.arrive_datetime.strftime('%H:%M')} "
                f"{ast.literal_eval(car.car_data)['body_code']} "
                f"{', '.join(ast.literal_eval(car.works))}"
                for car in cars_on_time]
        cars_string = '\n----------\n'.join(cars)
        markup = InlineKeyboardMarkup(confirm_time_keyboard)
        context.user_data['markup'] = markup
        await query.edit_message_text(f"На {date.strftime('%H:%M')} есть записи\n----------\n{cars_string}",
                                      reply_markup=markup)
        return 'CONFIRMING_TIME'
