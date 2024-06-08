"""
input_works function file
"""
from telegram import Update, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram_api.keyboards import save_works_keyboard


async def input_works(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """
    Function saves user input to context one by one, while user will not press save button.
    :param update: incoming update
    :param context: update context
    :return: next conversation state INPUT_WORKS
    """
    work = update.message.text
    context.user_data['new_car']['works'].append(work)
    work_list_text = '\n'.join(context.user_data['new_car']['works'])
    markup = InlineKeyboardMarkup(save_works_keyboard)
    context.user_data['markup'] = markup
    await update.message.reply_text(f'Список работ:\n{work_list_text}\nДобавьте работу, или сохраните список работ.',
                                    reply_markup=markup)
    return 'INPUT_WORKS'
