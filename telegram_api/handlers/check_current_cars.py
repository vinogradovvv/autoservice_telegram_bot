"""
Conversation handler for current cars.
"""
from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, filters, CallbackQueryHandler
from telegram_api.keyboards import workers_keyboard
from telegram_api.handlers.functions.show_calendar import show_calendar
from telegram_api.handlers.functions.show_cars import show_cars
from telegram_api.handlers.functions.cancel import cancel
from telegram_api.handlers.functions.cars_options import cars_options
from telegram_api.handlers.functions.comments import comments
from telegram_api.handlers.functions.add_comment import add_comment
from telegram_api.handlers.functions.edit_car import edit_car
from telegram_api.handlers.functions.edit_arrive_datetime import edit_arrive_datetime
from telegram_api.handlers.functions.choosing_date import choosing_date
from telegram_api.handlers.functions.choosing_time import choosing_time
from telegram_api.handlers.functions.confirm_date import confirm_date
from telegram_api.handlers.functions.confirm_time import confirm_time
from telegram_api.handlers.functions.choose_another_date import choose_another_date
from telegram_api.handlers.functions.choose_another_time import choose_another_time
from telegram_api.handlers.functions.edit_vin import edit_vin
from telegram_api.handlers.functions.input_vin import input_vin
from telegram_api.handlers.functions.input_body_code import input_body_code
from telegram_api.handlers.functions.save_vin import save_vin
from telegram_api.handlers.functions.input_vin_again import input_vin_again
from telegram_api.handlers.functions.edit_worker import edit_worker
from telegram_api.handlers.functions.choosing_worker import choosing_worker
from telegram_api.handlers.functions.delete_car import delete_car
from telegram_api.handlers.functions.close_car import close_car
from telegram_api.handlers.functions.order_parts import order_parts
from telegram_api.handlers.functions.input_parts import input_parts
from telegram_api.handlers.functions.save_parts import save_parts
from telegram_api.handlers.functions.choosing_filter import choosing_filter
from telegram_api.handlers.functions.choosing_part import choosing_part
from telegram_api.handlers.functions.input_price import input_price
from telegram_api.handlers.functions.choosing_product import choosing_product
from telegram_api.handlers.functions.choosing_offer import choosing_offer
from telegram_api.handlers.functions.choosing_quantity import choosing_quantity
from telegram_api.handlers.functions.add_to_cart import add_to_cart
from telegram_api.handlers.functions.list_cart import list_cart
from telegram_api.handlers.functions.remove_from_cart import remove_from_cart
from telegram_api.handlers.functions.remove_item import remove_item
from telegram_api.handlers.functions.delete_cart import delete_cart
from telegram_api.handlers.functions.wrong_input import wrong_input
from telegram_api.handlers.help import help_message

check_current_cars = ConversationHandler(
    entry_points=[MessageHandler(filters.Regex("^Открытые записи$"), show_calendar)],
    states={
        'SHOW_CARS': [
            CallbackQueryHandler(cancel, 'Cancel'),
            CallbackQueryHandler(show_cars)
        ],
        'CARS_OPTIONS': [
            CallbackQueryHandler(cancel, 'Cancel'),
            CallbackQueryHandler(cars_options)
        ],
        'CAR_ACTIONS': [
            CallbackQueryHandler(cancel, 'Cancel'),
            CallbackQueryHandler(comments, 'comments'),
            CallbackQueryHandler(edit_car, 'edit_car'),
            CallbackQueryHandler(edit_vin, 'edit_vin'),
            CallbackQueryHandler(order_parts, 'order_parts'),
            CallbackQueryHandler(list_cart, 'list_cart'),
            CallbackQueryHandler(delete_car, 'delete_car'),
            CallbackQueryHandler(close_car, 'close_car')
        ],
        'ADD_COMMENT': [
            CallbackQueryHandler(cancel, 'Cancel'),
            MessageHandler(filters.TEXT, add_comment),
            MessageHandler(filters.PHOTO, add_comment),
            MessageHandler(filters.VIDEO, add_comment)
        ],
        'EDIT_CAR': [
            CallbackQueryHandler(cancel, 'Cancel'),
            CallbackQueryHandler(edit_arrive_datetime, 'edit_arrive_datetime'),
            CallbackQueryHandler(edit_vin, 'edit_vin'),
            CallbackQueryHandler(edit_worker, 'edit_worker')
        ],
        'CHOOSING_DATE': [
            CallbackQueryHandler(cancel, 'Cancel'),
            CallbackQueryHandler(choosing_date)
        ],
        'CHOOSING_TIME': [
            CallbackQueryHandler(cancel, 'Cancel'),
            CallbackQueryHandler(choosing_time)
        ],
        'CONFIRMING_DATE': [
            CallbackQueryHandler(cancel, 'Cancel'),
            CallbackQueryHandler(confirm_date, 'confirm_date'),
            CallbackQueryHandler(choose_another_date, 'choose_another_date')
        ],
        'CONFIRMING_TIME': [
            CallbackQueryHandler(cancel, 'Cancel'),
            CallbackQueryHandler(confirm_time, 'confirm_time'),
            CallbackQueryHandler(choose_another_time, 'choose_another_time')
        ],
        'INPUT_VIN': [
            CallbackQueryHandler(cancel, 'Cancel'),
            MessageHandler(filters.TEXT, input_vin),
        ],
        'BAD_VIN': [
            CallbackQueryHandler(cancel, 'Cancel'),
            CallbackQueryHandler(save_vin, 'save_vin'),
            CallbackQueryHandler(input_vin_again, 'input_vin_again')
        ],
        'INPUT_BODY_CODE': [
            CallbackQueryHandler(cancel, 'Cancel'),
            MessageHandler(filters.TEXT, input_body_code),
        ],
        'CHOOSING_WORKER': [
            CallbackQueryHandler(cancel, 'Cancel'),
            CallbackQueryHandler(choosing_worker, workers_keyboard(workers_pattern=True))
        ],
        'INPUT_PARTS': [
            CallbackQueryHandler(cancel, 'Cancel'),
            MessageHandler(filters.TEXT, input_parts),
            CallbackQueryHandler(save_parts, 'save_parts')
        ],
        'CHOOSING_PART': [
            CallbackQueryHandler(cancel, 'Cancel'),
            CallbackQueryHandler(choosing_part)
        ],
        'CHOOSING_FILTER': [
            CallbackQueryHandler(cancel, 'Cancel'),
            CallbackQueryHandler(choosing_filter,
                                 r"^(choose_product|cheapest_one|most_expensive_one|price_range)$")
        ],
        'INPUT_PRICE': [
            CallbackQueryHandler(cancel, 'Cancel'),
            MessageHandler(filters.TEXT, input_price)
        ],
        'CHOOSING_PRODUCT': [
            CallbackQueryHandler(cancel, 'Cancel'),
            CallbackQueryHandler(choosing_product)
        ],
        'CHOOSING_OFFER': [
            CallbackQueryHandler(cancel, 'Cancel'),
            CallbackQueryHandler(choosing_offer)
        ],
        'CHOOSING_QUANTITY': [
            CallbackQueryHandler(cancel, 'Cancel'),
            MessageHandler(filters.TEXT, choosing_quantity),
            CallbackQueryHandler(add_to_cart)
        ],
        'ADD_TO_CART': [
            CallbackQueryHandler(cancel, 'Cancel'),
            CallbackQueryHandler(add_to_cart)
        ],
        'LIST_CART': [
            CallbackQueryHandler(cancel, 'Cancel'),
            CallbackQueryHandler(remove_from_cart, 'remove_from_cart'),
            CallbackQueryHandler(delete_cart, 'delete_cart')
        ],
        'REMOVE_FROM_CART': [
            CallbackQueryHandler(cancel, 'Cancel'),
            CallbackQueryHandler(remove_item)
        ]
    },
    fallbacks=[CommandHandler('help', help_message),
               CommandHandler('exit', help_message),
               MessageHandler(filters.TEXT, wrong_input)],
    allow_reentry=True
)
