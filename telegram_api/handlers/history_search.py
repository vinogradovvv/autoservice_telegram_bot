"""
Conversation handler for history search
"""
from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, filters, CallbackQueryHandler
from telegram_api.handlers.functions.vin_to_find import vin_to_find
from telegram_api.handlers.functions.cancel import cancel
from telegram_api.handlers.functions.input_vin import input_vin
from telegram_api.handlers.functions.wrong_input import wrong_input
from telegram_api.handlers.help import help_message

history_search = ConversationHandler(
    entry_points=[MessageHandler(filters.Regex("^Поиск в закрытых$"), vin_to_find)],
    states={
        'INPUT_VIN': [
            CallbackQueryHandler(cancel, 'Cancel'),
            MessageHandler(filters.TEXT, input_vin)
        ]
    },
    fallbacks=[CommandHandler('help', help_message),
               CommandHandler('exit', help_message),
               MessageHandler(filters.TEXT, wrong_input)],
    allow_reentry=True
)
