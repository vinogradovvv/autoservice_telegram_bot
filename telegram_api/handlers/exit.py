"""
Exit command handler file.
"""
from telegram.ext import CommandHandler
from telegram_api.handlers.functions.cancel import cancel

exit_handler = CommandHandler('exit', cancel)
