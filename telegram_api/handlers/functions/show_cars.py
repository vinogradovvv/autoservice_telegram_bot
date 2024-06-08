"""
show_cars function file
"""
from telegram import Update, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram_bot_calendar import WMonthTelegramCalendar
from telegram_api.keyboards import calendar_keyboard, cars_keyboard
from database.model.model import db, OpenedWorkOrders
from database.core import db_actions

db_read = db_actions.retrieve()


async def show_cars(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """
    Function asks user to choose the car, or another date if no cars this date
    :param update: incoming update
    :param context: update context
    :return: next conversation state
    """
    query = update.callback_query
    await query.answer()
    result, key, step = WMonthTelegramCalendar().process(query.data)
    if not result and key:
        if context.user_data['group'] == 'workers':
            marked_calendar = calendar_keyboard(calendar=key, worker=context.user_data['role'])
        else:
            marked_calendar = calendar_keyboard(calendar=key)
        context.user_data['markup'] = marked_calendar
        await query.edit_message_text("Выберите дату.",
                                      reply_markup=marked_calendar)

    elif result:
        cars_on_date = db_read(db, OpenedWorkOrders).where(
            OpenedWorkOrders.arrive_datetime.year == result.year and
            OpenedWorkOrders.arrive_datetime.month == result.month and
            OpenedWorkOrders.arrive_datetime.day == result.day
        )
        if context.user_data['group'] == 'workers':
            cars_on_date = cars_on_date.where(OpenedWorkOrders.worker == context.user_data['role'])
            marked_calendar = calendar_keyboard(worker=context.user_data['role'])
        else:
            marked_calendar = calendar_keyboard()
        if len(cars_on_date) == 0:
            context.user_data['markup'] = marked_calendar
            await query.edit_message_text(f'На {result} нет записей.\nВыберите другую дату',
                                          reply_markup=marked_calendar)
        else:
            markup = InlineKeyboardMarkup(cars_keyboard(cars_on_date))
            context.user_data['markup'] = markup
            await query.edit_message_text('Выберите запись.',
                                          reply_markup=markup)
            return 'CARS_OPTIONS'
