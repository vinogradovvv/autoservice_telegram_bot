"""
wrong_input function file
"""
from telegram import Update
from telegram.ext import ContextTypes


async def wrong_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Function tells user that his input is wrong
    and shows him last keyboard to use
    :param update: incoming update
    :param context: update context
    :return: None
    """
    query = update.callback_query
    try:
        await query.message.reply_text("Некорректный ввод", reply_markup=context.user_data['markup'])
    except AttributeError:
        await update.message.reply_text("Некорректный ввод", reply_markup=context.user_data['markup'])
    return None
