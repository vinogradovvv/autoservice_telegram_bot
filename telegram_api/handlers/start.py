"""
start function file
"""
import json
from warnings import filterwarnings
from settings import BotSettings
from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import ContextTypes, CommandHandler
from telegram_api.keyboards import role_choise_keyboard, admin_home_keyboard, worker_home_keyboard
from telegram.warnings import PTBUserWarning
from telegram_api.handlers.help import help_message

filterwarnings(action="ignore", message=r".*CallbackQueryHandler", category=PTBUserWarning)

bot_settings = BotSettings()
bot_demo = bot_settings.bot_demo


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Start function allows user to choose role in DEMO mode.
    In REAL mode function use data from crew.json file
    """
    context.user_data.clear()
    if bot_demo:
        await help_message(update, context)
        markup = ReplyKeyboardMarkup(role_choise_keyboard, one_time_keyboard=True)
        await update.message.reply_text("Выберите роль", reply_markup=markup)
    else:
        await help_message(update, context)
        with open('crew.json', 'r') as file:
            service = json.load(file)
        uid = str(update.effective_user.id)
        if uid in service['crew']['admins']:
            context.user_data['role'] = service['crew']['admins'][uid]['role']
            context.user_data['name'] = service['crew']['admins'][uid]['name']
            context.user_data['group'] = 'admins'
            context.user_data['uid'] = uid
            markup = ReplyKeyboardMarkup(admin_home_keyboard, one_time_keyboard=True)
        elif uid in service['crew']['workers']:
            context.user_data['role'] = service['crew']['workers'][uid]['role']
            context.user_data['name'] = service['crew']['workers'][uid]['name']
            context.user_data['group'] = 'workers'
            context.user_data['uid'] = uid
            markup = ReplyKeyboardMarkup(worker_home_keyboard, one_time_keyboard=True)
        else:
            return None
        await update.message.reply_text("Выберите действие", reply_markup=markup)

start_handler = CommandHandler('start', start)
