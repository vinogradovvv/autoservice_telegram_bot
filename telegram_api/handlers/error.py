"""
error function file
"""
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler
from telegram_api.keyboards import restart_keyboard
import logging

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                    level=logging.WARNING,
                    filename='bot.log')
logger = logging.getLogger(__name__)


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE) -> ConversationHandler.END:
    """
    Function handle errors logging them to file and asks user to restart
    by pressing button
    :param update: incoming update
    :param context: update context
    :return: ConversationHandler.END
    """
    uid = context.user_data['uid']
    logger.error(f"\n{'-' * 80}\nException while handling an update:", exc_info=context.error)
    await context.bot.send_message(chat_id=uid,
                                   text='Произошла ошибка!\nНажмите на кнопку, чтобы перезапустить.',
                                   reply_markup=ReplyKeyboardMarkup(restart_keyboard))
    context.user_data.clear()
    return ConversationHandler.END
