"""
input_comment function file
"""
import json
from datetime import datetime
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler
from telegram_api.keyboards import admin_home_keyboard
from database.model.model import db, OpenedWorkOrders
from database.core import db_actions
from settings import BotSettings

bot_settings = BotSettings()
bot_demo = bot_settings.bot_demo
db_write = db_actions.create()


async def input_comment(update: Update, context: ContextTypes.DEFAULT_TYPE) -> ConversationHandler.END:
    """
    Function saves user input as comment in context.
    Then write data from context to database.
    :param update: incoming update
    :param context: update context
    :return: END attribute of ConversationHandler class
    """
    car_comment = []
    comment = {}
    if update.message.text:
        comment['type'] = 'text'
        comment['message'] = update.message.text
    elif update.message.photo:
        comment['type'] = 'photo'
        comment['message'] = update.message.photo[0].file_id
    elif update.message.video:
        comment['type'] = 'video'
        comment['message'] = update.message.video['file_id']
    comment['date'] = datetime.now().strftime("%d/%m/%Y, %H:%M")
    comment['name'] = context.user_data['name']
    car_comment.append(comment)
    comment_json = json.dumps(car_comment)
    context.user_data['new_car']['comment'] = comment_json
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
    await update.message.reply_text('Запись сохранена', reply_markup=markup)
    context.user_data['new_car'] = {}
    context.user_data['mode'] = None
    return ConversationHandler.END
