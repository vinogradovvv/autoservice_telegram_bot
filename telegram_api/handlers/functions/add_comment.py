"""
add_comment function file
"""
import json
from datetime import datetime
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler
from telegram_api.keyboards import worker_home_keyboard, admin_home_keyboard
from database.model.model import db, OpenedWorkOrders
from database.core import db_actions

db_get = db_actions.get()
db_update = db_actions.update()


async def add_comment(update: Update, context: ContextTypes.DEFAULT_TYPE) -> ConversationHandler.END:
    """
    Function saves comment of TEXT, PHOTO or VIDEO type to the database
    :param update: incoming update
    :param context: update context
    :return: END attribute of ConversationHandler class
    """
    car = db_get(db, OpenedWorkOrders, OpenedWorkOrders.id == context.user_data['car_id'])
    car_comments = json.loads(car.comment)
    new_comment = {}
    if update.message.text:
        new_comment['type'] = 'text'
        new_comment['message'] = update.message.text
    elif update.message.photo:
        new_comment['type'] = 'photo'
        new_comment['message'] = update.message.photo[0].file_id
    elif update.message.video:
        new_comment['type'] = 'video'
        new_comment['message'] = update.message.video['file_id']
    new_comment['date'] = datetime.now().strftime("%d/%m/%Y, %H:%M")
    new_comment['name'] = context.user_data['name']
    car_comments.append(new_comment)
    comments_json = json.dumps(car_comments)
    db_update(db, OpenedWorkOrders, context.user_data['car_id'], 'comment', comments_json)
    if context.user_data['group'] == 'workers':
        markup = worker_home_keyboard
    else:
        markup = admin_home_keyboard
    context.user_data['markup'] = markup
    await update.message.reply_text('Коментарий сохранен',
                                    reply_markup=ReplyKeyboardMarkup(markup, one_time_keyboard=True))
    context.user_data['cars_on_date'] = []
    context.user_data['car_id'] = ''
    return ConversationHandler.END
