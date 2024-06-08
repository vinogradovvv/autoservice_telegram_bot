"""
role_choice function file
"""
from typing import Optional
from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import ContextTypes, MessageHandler, filters, ConversationHandler
from telegram_api.keyboards import admin_home_keyboard, worker_home_keyboard


async def role_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> Optional[ConversationHandler.END]:
    """
    Function works in DEMO mode. It saves user role, gives action choose keyboard, and waits for user choice
    :param update: incoming update
    :param context: update context
    :return: None or ConversationHandler.END
    """
    context.user_data['role'] = update.message.text
    if context.user_data['role'] == 'Директор':
        context.user_data['name'] = 'Данил'
        context.user_data['group'] = 'admins'
        context.user_data['uid'] = str(update.effective_user.id)
        markup = ReplyKeyboardMarkup(admin_home_keyboard, one_time_keyboard=True)
    elif context.user_data['role'] == 'Электрик':
        context.user_data['name'] = 'Владимир'
        context.user_data['group'] = 'workers'
        context.user_data['uid'] = str(update.effective_user.id)
        markup = ReplyKeyboardMarkup(worker_home_keyboard, one_time_keyboard=True)
    elif context.user_data['role'] == 'Механик':
        context.user_data['name'] = 'Александр'
        context.user_data['group'] = 'workers'
        context.user_data['uid'] = str(update.effective_user.id)
        markup = ReplyKeyboardMarkup(worker_home_keyboard, one_time_keyboard=True)
    else:
        return ConversationHandler.END
    await update.message.reply_text("Выберите действие", reply_markup=markup)

role_choice_handler = MessageHandler(filters.Regex("^(Директор|Механик|Электрик)$"), role_choice)
