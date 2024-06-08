"""
save_works function file
"""
from telegram import Update, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram_api.keyboards import skip_comment_keyboard


async def save_works(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """
    Function asks user to input comment, and gives him button to skip.
    :param update: incoming update
    :param context: update context
    :return: next conversation state INPUT_PARTS
    """
    query = update.callback_query
    markup = InlineKeyboardMarkup(skip_comment_keyboard)
    context.user_data['markup'] = markup
    await query.edit_message_text('Введите комментарий',
                                  reply_markup=markup)
    return 'INPUT_COMMENT'
