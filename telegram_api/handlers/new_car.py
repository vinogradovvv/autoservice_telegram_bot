"""
Conversation handler for adding new car
"""
from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, filters, CallbackQueryHandler
from telegram_api.keyboards import workers_keyboard
from telegram_api.handlers.functions.add_new_car import add_new_car
from telegram_api.handlers.functions.choosing_date import choosing_date
from telegram_api.handlers.functions.confirm_date import confirm_date
from telegram_api.handlers.functions.choose_another_date import choose_another_date
from telegram_api.handlers.functions.choosing_time import choosing_time
from telegram_api.handlers.functions.confirm_time import confirm_time
from telegram_api.handlers.functions.choose_another_time import choose_another_time
from telegram_api.handlers.functions.choosing_worker import choosing_worker
from telegram_api.handlers.functions.input_vin import input_vin
from telegram_api.handlers.functions.input_vin_again import input_vin_again
from telegram_api.handlers.functions.skip_vin import skip_vin
from telegram_api.handlers.functions.save_vin import save_vin
from telegram_api.handlers.functions.input_body_code import input_body_code
from telegram_api.handlers.functions.input_kilometres import input_kilometres
from telegram_api.handlers.functions.input_works import input_works
from telegram_api.handlers.functions.save_works import save_works
from telegram_api.handlers.functions.input_comment import input_comment
from telegram_api.handlers.functions.skip_comment import skip_comment
from telegram_api.handlers.functions.cancel import cancel
from telegram_api.handlers.functions.wrong_input import wrong_input
from telegram_api.handlers.help import help_message


add_car_handler = ConversationHandler(
    entry_points=[MessageHandler(filters.Regex("^Добавить запись$"), add_new_car)],
    states={
        'CHOOSING_DATE': [
            CallbackQueryHandler(cancel, 'Cancel'),
            CallbackQueryHandler(choosing_date)
        ],
        'CHOOSING_TIME': [
            CallbackQueryHandler(cancel, 'Cancel'),
            CallbackQueryHandler(choosing_time)
        ],
        'CHOOSING_WORKER': [
            CallbackQueryHandler(cancel, 'Cancel'),
            CallbackQueryHandler(choosing_worker, workers_keyboard(workers_pattern=True))
        ],
        'INPUT_VIN': [
            CallbackQueryHandler(cancel, 'Cancel'),
            MessageHandler(filters.TEXT, input_vin),
            CallbackQueryHandler(skip_vin, 'skip_vin')
        ],
        'INPUT_BODY_CODE': [
            CallbackQueryHandler(cancel, 'Cancel'),
            MessageHandler(filters.TEXT, input_body_code),
        ],
        'INPUT_KILOMETRES': [
            CallbackQueryHandler(cancel, 'Cancel'),
            MessageHandler(filters.Regex(r'^\d+$'), input_kilometres)
        ],
        'INPUT_WORKS': [
            CallbackQueryHandler(cancel, 'Cancel'),
            MessageHandler(filters.TEXT, input_works),
            CallbackQueryHandler(save_works, 'save_works')
        ],
        'INPUT_COMMENT': [
            CallbackQueryHandler(cancel, 'Cancel'),
            MessageHandler(filters.TEXT, input_comment),
            MessageHandler(filters.PHOTO, input_comment),
            MessageHandler(filters.VIDEO, input_comment),
            CallbackQueryHandler(skip_comment, 'skip_comment')
        ],
        'BAD_VIN': [
            CallbackQueryHandler(cancel, 'Cancel'),
            CallbackQueryHandler(save_vin, 'save_vin'),
            CallbackQueryHandler(input_vin_again, 'input_vin_again')
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
        ]
    },
    fallbacks=[CommandHandler('help', help_message),
               CommandHandler('exit', help_message),
               MessageHandler(filters.TEXT, wrong_input)],
    allow_reentry=True
)
