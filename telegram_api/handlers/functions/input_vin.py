"""
input_vin function
"""
import re
import ast
from telegram import Update, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler
from telegram_api.keyboards import vin_keyboard, admin_home_keyboard, worker_home_keyboard, cancel_button
from bmw_decode.core import bmw_decoder
from database.model.model import db, OpenedWorkOrders, ClosedWorkOrders
from database.core import db_actions

db_update = db_actions.update()
db_read = db_actions.retrieve()
decode_vin = bmw_decoder.decode_vin()


async def input_vin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> [str, ConversationHandler.END]:
    """
    Function checks user input. If it is 7 symbols length try's to decode it.
    If decoded parse data to context, and return INPUT_KILOMETRES state. If it
    doesn't decode tell's user about it, and return BAD_VIN state. If VIN
    doesn't match check expression tells user about it, and return INPUT_VIN state.
    :param update: incoming update
    :param context: update context
    :return: next conversation state or ConversationHandler.END
    """
    vin = update.message.text.upper()
    if re.match(r'^\w{7}$', vin):
        if context.user_data['mode'] == 'add_new_car':
            car_data = decode_vin(vin)
            context.user_data['new_car']['vin_code'] = vin
            context.user_data['new_car']['car_data'] = car_data
            if len(car_data) > 1:
                markup = InlineKeyboardMarkup([cancel_button])
                context.user_data['markup'] = markup
                await update.message.reply_text(f"{context.user_data['new_car']['car_data']['body_code']} "
                                                f"{context.user_data['new_car']['car_data']['model']}"
                                                f"\nВведите пробег",
                                                reply_markup=markup)
                return 'INPUT_KILOMETRES'
            else:
                markup = InlineKeyboardMarkup(vin_keyboard)
                context.user_data['markup'] = markup
                await update.message.reply_text(
                    f"VIN {vin} не декодируется.\nЕсли VIN введен верно, добавьте коментарий "
                    f"с информации об автомобиле.\nЕсли допущена ошибка нажмите кнопку "
                    f"'Ввести VIN заново'.",
                    reply_markup=markup)
                return 'BAD_VIN'
        elif context.user_data['mode'] == 'edit_car':
            car_data = decode_vin(vin)
            context.user_data['car_vin'] = vin
            context.user_data['car_data'] = car_data
            if len(car_data) > 1:
                db_update(db,
                          OpenedWorkOrders,
                          context.user_data['car_id'],
                          'car_data',
                          car_data)
                db_update(db,
                          OpenedWorkOrders,
                          context.user_data['car_id'],
                          'vin_code',
                          vin)
                if context.user_data['group'] == 'admins':
                    markup = ReplyKeyboardMarkup(admin_home_keyboard)
                else:
                    markup = ReplyKeyboardMarkup(worker_home_keyboard, one_time_keyboard=True)
                context.user_data['markup'] = markup
                await update.message.reply_text('Запись сохранена',
                                                reply_markup=markup)
                return ConversationHandler.END
            else:
                markup = InlineKeyboardMarkup(vin_keyboard)
                context.user_data['markup'] = markup
                await update.message.reply_text(
                    f"VIN {vin} не декодируется.\nЕсли VIN введен верно, добавьте коментарий "
                    f"с информации об автомобиле.\nЕсли допущена ошибка нажмите кнопку "
                    f"'Ввести VIN заново'.",
                    reply_markup=markup)
                return 'BAD_VIN'
        elif context.user_data['mode'] == 'history_search':
            car_history = db_read(db, ClosedWorkOrders).where(ClosedWorkOrders.vin_code == vin)
            if len(car_history) > 0:
                message = '\n\n'.join(
                    [f'{car.close_datetime.strftime("%d/%m/%Y")}\n'
                     f'Пробег: {car.kilometres} км.\n'
                     f'Исполнитель: {car.worker}\n'
                     f'{", ".join(ast.literal_eval(car.works))}' for car in car_history])
            else:
                message = f'Автомобиль с VIN {vin} в истории не найден.'
            context.user_data['mode'] = ''
            if context.user_data['group'] == 'admins':
                keyboard = admin_home_keyboard
            else:
                keyboard = worker_home_keyboard
            markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
            context.user_data['markup'] = markup
            await update.message.reply_text(message,
                                            reply_markup=markup)
            return ConversationHandler.END
    else:
        markup = InlineKeyboardMarkup([cancel_button])
        context.user_data['markup'] = markup
        await update.message.reply_text("Некорректный VIN код!\nВведите последние 7 символов VIN",
                                        reply_markup=markup)
        return 'INPUT_VIN'
