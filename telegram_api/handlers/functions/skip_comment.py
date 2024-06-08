"""
skip_comment function file
"""
import json
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler
from telegram_api.keyboards import admin_home_keyboard
from settings import BotSettings
from database.model.model import db, OpenedWorkOrders
from database.core import db_actions

bot_settings = BotSettings()
bot_demo = bot_settings.bot_demo
db_write = db_actions.create()


async def skip_comment(update: Update, context: ContextTypes.DEFAULT_TYPE) -> ConversationHandler.END:
    """
    Function saves car data from context to database, clears car data, ends the conversation
    :param update: incoming update
    :param context: update context
    :return: ConversationHandler.END
    """
    query = update.callback_query
    db_write(db, OpenedWorkOrders, context.user_data['new_car'])
    if not bot_demo:
        with open('crew.json', 'r') as file:
            service = json.load(file)
            role = context.user_data['new_car']['worker']
            for worker, data in service['crew']['workers'].items():
                if data['role'] == role:
                    await context.bot.send_message(chat_id=worker,
                                                   text=f"Добавлена запись на "
                                                        f"{context.user_data['new_car']['arrive_datetime']}",
                                                   reply_markup=None)
    markup = ReplyKeyboardMarkup(admin_home_keyboard, one_time_keyboard=True)
    context.user_data['markup'] = markup
    await query.message.reply_text('Запись сохранена',
                                   reply_markup=markup)
    context.user_data['new_car'] = {}
    context.user_data['mode'] = None
    return ConversationHandler.END
