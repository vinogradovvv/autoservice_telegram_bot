"""
comments function file
"""
import json
from telegram import Update, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram_api.keyboards import cancel_button
from database.model.model import db, OpenedWorkOrders
from database.core import db_actions

db_get = db_actions.get()


async def comments(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """
    Function shows comments to chosen car
    :param update: incoming update
    :param context: update context
    :return: next conversation state
    """
    query = update.callback_query
    car = db_get(db, OpenedWorkOrders, OpenedWorkOrders.id == context.user_data['car_id'])
    car_comments = json.loads(car.comment)
    for comment in car_comments:
        if comment['type'] == 'text':
            await query.message.reply_text(f"{comment['date']} {comment['name']}\n{comment['message']}")
        elif comment['type'] == 'photo':
            await query.message.reply_text(f"{comment['date']} {comment['name']}")
            await query.message.reply_photo(comment['message'])
        elif comment['type'] == 'video':
            await query.message.reply_text(f"{comment['date']} {comment['name']}")
            await query.message.reply_video(comment['message'])
    text = '\n\n Что-бы добавить коментарий, отправьте его ответным сообщением.'
    markup = InlineKeyboardMarkup([cancel_button])
    context.user_data['markup'] = markup
    await query.message.reply_text(text, reply_markup=markup)
    return 'ADD_COMMENT'
