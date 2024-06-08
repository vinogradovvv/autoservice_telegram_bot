"""
help command handler file
"""
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler


async def help_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Function shows user help message
    :param update: incoming update
    :param context: update context
    :return: None
    """
    message = ('Команды бота:\n\t'
               '/start - Запуск бота.\nЕсли бот не реагирует введите "/start".\n\t'
               '/exit - Перезапустит ваш диалог и вернет вас в начало.\n\t'
               '/help - Помощь по командам.')
    await update.message.reply_text(message)

help_handler = CommandHandler('help', help_message)
