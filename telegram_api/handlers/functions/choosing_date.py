"""
choosing_date function file
"""
import ast
from telegram import Update, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram_bot_calendar import WMonthTelegramCalendar
from telegram_api.keyboards import time_keyboard, confirm_date_keyboard, calendar_keyboard
from database.model.model import db, OpenedWorkOrders
from database.core import db_actions

db_read = db_actions.retrieve()


async def choosing_date(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """
    Function process button pressing, and if date button was pressed and this date is free
    saves date to context and returns CHOOSING_TIME state. If chosen date is busy
    tels user about it and returns CONFIRMING_DATE state. If pressed button was not date button
    (next o previous month button) recreates calendar keyboard, mark it with busy days,
    and waits user to press calendar button.
    :param update: incoming update
    :param context: update context
    :return: next conversation state CHOOSING_TIME or CONFIRMING_DATE.
    """
    query = update.callback_query
    await query.answer()
    result, key, step = WMonthTelegramCalendar().process(query.data)
    if not result and key:
        marked_calendar = calendar_keyboard(calendar=key)
        context.user_data['markup'] = marked_calendar
        await query.edit_message_text("Выберите дату.",
                                      reply_markup=marked_calendar)
    elif result:
        if context.user_data['mode'] == 'add_new_car':
            context.user_data['new_car']['arrive_datetime'] = result
        elif context.user_data['mode'] == 'edit_car':
            context.user_data['car_arrive'] = result
        cars_on_date = db_read(db, OpenedWorkOrders).where(
            OpenedWorkOrders.arrive_datetime.year == result.year and
            OpenedWorkOrders.arrive_datetime.month == result.month and
            OpenedWorkOrders.arrive_datetime.day == result.day
        )
        if len(cars_on_date) == 0:
            markup = InlineKeyboardMarkup(time_keyboard())
            context.user_data['markup'] = markup
            await query.edit_message_text(f"{result}\nВо сколько?",
                                          reply_markup=markup)
            return 'CHOOSING_TIME'
        else:
            context.user_data['cars_on_date'] = cars_on_date
            cars = [f"{car.worker} "
                    f"{car.arrive_datetime.strftime('%H:%M')} "
                    f"{ast.literal_eval(car.car_data)['body_code']} "
                    f"{', '.join(ast.literal_eval(car.works))}"
                    for car in cars_on_date]
            cars_string = '\n----------\n'.join(cars)
            markup = InlineKeyboardMarkup(confirm_date_keyboard)
            context.user_data['markup'] = markup
            await query.edit_message_text(f"На {result} число есть записи\n----------\n{cars_string}",
                                          reply_markup=markup)
            return 'CONFIRMING_DATE'
