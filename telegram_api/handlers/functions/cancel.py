"""
cancel function file
"""
import json
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler
from telegram_api.keyboards import role_choise_keyboard, admin_home_keyboard, worker_home_keyboard
from settings import BotSettings

bot_settings = BotSettings()
bot_demo = bot_settings.bot_demo


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> ConversationHandler.END:
    """
    Function clear user data and asks user of his role in DEMO mode
    or use data from 'crew.json' file in REAL mode.
    :param update: incoming update
    :param context: update context
    :return: None
    """
    query = update.callback_query
    context.user_data.clear()
    if bot_demo:
        markup = ReplyKeyboardMarkup(role_choise_keyboard, one_time_keyboard=True)
        context.user_data['markup'] = markup
        try:
            await query.message.reply_text("Выберите роль", reply_markup=markup)
        except AttributeError:
            await update.message.reply_text("Выберите роль", reply_markup=markup)
        return ConversationHandler.END
    else:
        with open('crew.json', 'r') as file:
            service = json.load(file)
        uid = str(update.effective_user.id)
        if uid in service['crew']['admins']:
            context.user_data['role'] = service['crew']['admins'][uid]['role']
            context.user_data['name'] = service['crew']['admins'][uid]['name']
            context.user_data['group'] = 'admins'
            markup = ReplyKeyboardMarkup(admin_home_keyboard, one_time_keyboard=True)
        elif uid in service['crew']['workers']:
            context.user_data['role'] = service['crew']['workers'][uid]['role']
            context.user_data['name'] = service['crew']['workers'][uid]['name']
            context.user_data['group'] = 'workers'
            markup = ReplyKeyboardMarkup(worker_home_keyboard, one_time_keyboard=True)
        else:
            return ConversationHandler.END
        context.user_data['markup'] = markup
        try:
            await query.message.reply_text("Выберите действие", reply_markup=markup)
        except AttributeError:
            await update.message.reply_text("Выберите действие", reply_markup=markup)
        return ConversationHandler.END
