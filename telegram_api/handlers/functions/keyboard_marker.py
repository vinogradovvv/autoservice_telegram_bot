"""
File contain functions of marking keyboards
"""
import datetime
import json
from telegram import InlineKeyboardButton
from telegram_bot_calendar import WMonthTelegramCalendar


def mark_dates(calendar_keyboard: WMonthTelegramCalendar.build, cars_dates: list[str]) -> WMonthTelegramCalendar.build:
    """
    Function update buttons of given calendar keyboard.
    :param calendar_keyboard: calendar keyboard
    :param cars_dates: busy dates
    :return: marked calendar keyboard
    """
    calendar = json.loads(calendar_keyboard)
    for row in calendar['inline_keyboard']:
        for button in row:
            if isinstance(button['text'], int):
                date_string = button['callback_data'][12:]
                date = datetime.datetime.strptime(date_string, '%Y_%m_%d').date()
                if date in cars_dates:
                    button['text'] = f"-{button['text']}-"
    marked_calendar = json.dumps(calendar)
    return marked_calendar


def mark_times(time_keyboard: list[list[InlineKeyboardButton]], cars_times: list[str])\
        -> list[list[InlineKeyboardButton]]:
    """
    Function update buttons of given inline keyboard.
    :param time_keyboard: time inline keyboard
    :param cars_times: busy times
    :return: marked inline keyboard
    """
    for row in time_keyboard:
        for key in row:
            if key.text in cars_times:
                button_text = f"-{key.text}-"
                button = InlineKeyboardButton(button_text, callback_data=button_text)
                time_keyboard[time_keyboard.index(row)][row.index(key)] = button
    return time_keyboard


def mark_workers(workers_keyboard: list[list[InlineKeyboardButton]], busy_workers: list[str])\
        -> list[list[InlineKeyboardButton]]:
    """
    Function recreates workers keyboard without workers, who are busy at this time.
    :param workers_keyboard: workers inline keyboard
    :param busy_workers: workers, busy at this time
    :return: updated workers inline keyboard
    """
    marked_keyboard = []
    for row in workers_keyboard:
        marked_row = []
        for key in row:
            if key.text in busy_workers:
                continue
            marked_row.append(key)
        if len(marked_row) > 0:
            marked_keyboard.append(marked_row)
    return marked_keyboard
