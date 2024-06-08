"""
This file contains all keyboards
"""
import json
import ast
from typing import Dict, List, Optional
from peewee import ModelSelect, Model
from telegram import InlineKeyboardButton
from telegram_bot_calendar import WMonthTelegramCalendar
from telegram_api.handlers.functions.keyboard_marker import mark_dates
from settings import EuroautoSettings
from database.model.model import db, OpenedWorkOrders
from database.core import db_actions

euroauto = EuroautoSettings()

db_read = db_actions.retrieve()

cancel_button = [InlineKeyboardButton('Отмена', callback_data='Cancel')]

restart_keyboard = [['/start']]

role_choise_keyboard = [
    ["Директор"],
    ["Механик", "Электрик"],
]

admin_home_keyboard = [
    ["Открытые записи"],
    ["Добавить запись"],
    ["Поиск в закрытых"]
]

worker_home_keyboard = [
    ["Открытые записи"],
    ["Поиск в закрытых"]
]

skip_vin_keyboard = [[InlineKeyboardButton('Пропустить', callback_data='skip_vin')], cancel_button]

skip_comment_keyboard = [[InlineKeyboardButton('Пропустить', callback_data='skip_comment')], cancel_button]

save_parts_keyboard = [[InlineKeyboardButton('Сохранить запчасти', callback_data='save_parts')], cancel_button]

save_works_keyboard = [[InlineKeyboardButton('Сохранить работы', callback_data='save_works')], cancel_button]

vin_keyboard = [
    [InlineKeyboardButton('Сохранить VIN', callback_data='save_vin')],
    [InlineKeyboardButton('Ввести VIN заново', callback_data='input_vin_again')],
    cancel_button
]

confirm_date_keyboard = [
    [InlineKeyboardButton('Записать на выбранную дату', callback_data='confirm_date')],
    [InlineKeyboardButton('Выбрать другую дату', callback_data='choose_another_date')],
    cancel_button
]

confirm_time_keyboard = [
    [InlineKeyboardButton('Записать на выбранное время', callback_data='confirm_time')],
    [InlineKeyboardButton('Выбрать другое время', callback_data='choose_another_time')],
    cancel_button
]

choose_another_time_keyboard = [[InlineKeyboardButton('Выбрать другое время', callback_data='choose_another_time')],
                                cancel_button]

edit_car_keyboard = [[InlineKeyboardButton('Изменить дату/время приезда', callback_data='edit_arrive_datetime')],
                     [InlineKeyboardButton('Изменить VIN', callback_data='edit_vin')],
                     [InlineKeyboardButton('Изменить исполнителя', callback_data='edit_worker')],
                     cancel_button]

filters_keyboard = [[InlineKeyboardButton('Все варианты', callback_data='choose_product')],
                    [InlineKeyboardButton('Самый дешевый', callback_data='cheapest_one')],
                    [InlineKeyboardButton('Самый дорогой', callback_data='most_expensive_one')],
                    [InlineKeyboardButton('Диапазон цен', callback_data='price_range')],
                    cancel_button]

cart_keyboard = [[InlineKeyboardButton('Удалить позицию', callback_data='remove_from_cart')],
                 [InlineKeyboardButton('Удалить корзину', callback_data='delete_cart')],
                 cancel_button]


def calendar_keyboard(calendar=None, worker: str = None) -> WMonthTelegramCalendar.build:
    """
    Function generates calendar keyboard if it was not given, and marks busy dates
    :param calendar: calendar keyboard to mark the dates.
    :param worker: worker, who's busy days need to be marked. If None busy days of all workers will be marked.
    :return: calendar keyboard with marked busy days
    """
    if not calendar:
        calendar, step = WMonthTelegramCalendar().build()
    if worker:
        cars = db_read(db, OpenedWorkOrders).where(OpenedWorkOrders.worker == worker)
        cars_dates = [car.arrive_datetime.date() for car in cars]
        marked_calendar = mark_dates(calendar, cars_dates)
    else:
        cars = db_read(db, OpenedWorkOrders)
        cars_dates = [car.arrive_datetime.date() for car in cars]
        marked_calendar = mark_dates(calendar, cars_dates)
    marked_calendar = marked_calendar.replace(' []', ' [{"callback_data": "Cancel", "text": "Отмена"}]')
    return marked_calendar


def time_keyboard() -> list[list[InlineKeyboardButton]]:
    """
    Function generates keyboard to choose arrive time
    :return: time keyboard
    """
    keyboard = []
    for hours in range(10, 20):
        row = []
        for minutes in range(2):
            if minutes == 0:
                time_string = f'{hours}:00'
            else:
                time_string = f'{hours}:30'
            row.append(InlineKeyboardButton(time_string, callback_data=time_string))
        keyboard.append(row)
    keyboard.append(cancel_button)
    return keyboard


def workers_keyboard(workers_pattern: bool = False) -> str | list[list[InlineKeyboardButton]]:
    """
    Function generates either filter pattern string, or keyboard to choose the worker
    :param workers_pattern: True if you need filter pattern string, False if you need keyboard
    :return: string / list of workers buttons
    """
    with open('crew.json', 'r') as file:
        service = json.load(file)
        if workers_pattern:
            workers = [worker['role'] for worker in service['crew']['workers'].values()]
            workers_str = f'({"|".join(workers)})'
            return workers_str
        else:
            keyboard = [[InlineKeyboardButton(worker['role'], callback_data=worker['role'])
                         for worker in service['crew']['workers'].values()], cancel_button]
            return keyboard


def cars_keyboard(cars: ModelSelect) -> list[list[InlineKeyboardButton]]:
    """
    Function generates keyboard to choose the car
    :param cars: select object from database
    :return: list of cars buttons
    """
    keyboard = []
    for car in cars:
        car_data = ast.literal_eval(car.car_data)
        body_code = car_data['body_code']
        if 'model' in car_data:
            model = car_data['model']
        else:
            model = 'NO VIN'
        arrive = car.arrive_datetime.strftime('%H:%M')
        button_text = ' '.join([body_code, model, arrive])
        keyboard.append([InlineKeyboardButton(button_text, callback_data=car.id)])
    keyboard.append(cancel_button)
    return keyboard


def workers_options_keyboard(car: Model) -> list[list[InlineKeyboardButton]]:
    """
    Function generates keyboard of worker car options buttons
    :param car: peewee model containing car info
    :return: list of options buttons
    """
    keyboard = [[InlineKeyboardButton(text='Каталог', url=ast.literal_eval(car.car_data)['catalog_link'])],
                [InlineKeyboardButton(text='Коментарии', callback_data='comments')],
                cancel_button]
    if not car.vin_code:
        keyboard.insert(0, [InlineKeyboardButton(text='Ввести VIN', callback_data='edit_vin')])
    return keyboard


def admins_options_keyboard(car: Model) -> list[list[InlineKeyboardButton]]:
    """
    Function generates keyboard of administrator car options buttons
    :param car: peewee model containing car info
    :return: list of options buttons
    """
    keyboard = [[InlineKeyboardButton(text='Каталог', url=ast.literal_eval(car.car_data)['catalog_link'])],
                [InlineKeyboardButton(text='Коментарии', callback_data='comments')],
                [InlineKeyboardButton(text='Редактировать запись', callback_data='edit_car')],
                # [InlineKeyboardButton(text='Заказать запчасти', callback_data='order_parts')],
                # [InlineKeyboardButton(text='Корзина Euroauto', callback_data='list_cart')],
                [InlineKeyboardButton(text='Отправить в выполненные', callback_data='close_car')],
                [InlineKeyboardButton(text='Удалить', callback_data='delete_car')]]
    if euroauto.login and euroauto.password:
        keyboard.append([InlineKeyboardButton(text='Заказать запчасти', callback_data='order_parts')])
        keyboard.append([InlineKeyboardButton(text='Корзина Euroauto', callback_data='list_cart')])
    keyboard.append(cancel_button)
    return keyboard


def parts_keyboard(parts: Dict) -> list[list[InlineKeyboardButton]]:
    """
    Function generates keyboard of parts buttons to choose spare part to order
    :param parts: dict with info about spare parts needed for fix the car
    :return: list of parts buttons
    """
    keyboard = [[InlineKeyboardButton(text=part_key, callback_data=part_number)]
                for part_number, part_key in parts.items()]
    keyboard.append(cancel_button)
    return keyboard


def products_keyboard(keyboard_data: Dict,
                      product_filter: str,
                      price_min: Optional[int] = None,
                      price_max: Optional[int] = None) -> list[list[InlineKeyboardButton]]:
    """
    Function generates keyboard of products with price buttons
    :param price_max: maximum price
    :param price_min: minimum price
    :param product_filter: search filter
    :param keyboard_data: dict with info about available products
    :return: list of products buttons
    """
    if product_filter == 'cheapest_one':
        data = keyboard_data.items()
        cheap_one = next(iter(data))
        keyboard_data = {cheap_one[0]: cheap_one[1]}
    elif product_filter == 'most_expensive_one':
        data = keyboard_data.items()
        expensive_one = next(reversed(data))
        keyboard_data = {expensive_one[0]: expensive_one[1]}
    elif product_filter == 'price_range':
        new_keyboard_data = {}
        for key, value in keyboard_data.items():
            for price in value['prices']:
                if price_min < price < price_max:
                    new_keyboard_data[key] = value
        keyboard_data = new_keyboard_data

    keyboard = [[InlineKeyboardButton(text=f'{name}: {", ".join(str(price) for price in data["prices"])}',
                                      callback_data=data['product_id'])]
                for name, data in keyboard_data.items()]

    keyboard.append(cancel_button)
    return keyboard


def offers_keyboard(keyboard_data: List[Dict]) -> list[list[InlineKeyboardButton]]:
    """
    Function generates keyboard of offers with in stock amount buttons
    :param keyboard_data: list of dicts with info about available ofers
    :return: list of offers buttons
    """
    keyboard = [[InlineKeyboardButton(text=f'{offer["quantity"]}шт. {offer["store"]}',
                                      callback_data=f'{offer["id"]},{offer["quantity"]}')] for offer in keyboard_data]
    keyboard.append(cancel_button)
    return keyboard


def add_to_cart_keyboard(offer_id: str, quantity: int = 1) -> list[list[InlineKeyboardButton]]:
    """
    Function generates keyboard with add to cart button with given quantity
    :param offer_id: euroauto offer id
    :param quantity: amount of parts
    :return: list of add to cart, and cancel buttons
    """
    keyboard = [[InlineKeyboardButton(text=f'Добавить в корзину {quantity} шт.',
                                      callback_data=f'{offer_id}, {quantity}')],
                cancel_button]
    return keyboard


def cart_items_keyboard(data: Dict) -> list[list[InlineKeyboardButton]]:
    """

    :param data: dict of Euroauto cart items
    :return: cart items keyboard
    """
    keyboard = []
    for item in data['items']:
        brand = data['manufacturer_codes'][data['products'][item['product_id']]['manufacturer_code']]['manufacturer']['name']
        code = data['manufacturer_codes'][data['products'][item['product_id']]['manufacturer_code']]['code']
        offer_id = item['offer_id']
        keyboard.append([InlineKeyboardButton(text=f'{code} {brand}', callback_data=offer_id)])
    keyboard.append(cancel_button)
    return keyboard
