"""
input_parts function file
"""
from telegram import Update, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram_api.keyboards import save_parts_keyboard
from bmw_decode.core import bmw_decoder

decode_part_number = bmw_decoder.decode_part_number()


async def input_parts(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """
    Function asks user to input catalog part numbers one by one, and saves them to list in context.
    :param update: incoming update
    :param context: update context
    :return: INPUT_PARTS state
    """
    part_number = update.message.text.replace(' ', '')
    link = context.user_data['car_link']
    part_name = decode_part_number(part_number)
    if part_name:
        context.user_data['car_parts'][part_number] = part_name
        parts_list = [f'{number} - {name}' for number, name in context.user_data['car_parts'].items()]
        parts_list_text = '\n'.join(parts_list)
        markup = InlineKeyboardMarkup(save_parts_keyboard)
        context.user_data['markup'] = markup
        await update.message.reply_text(f'{parts_list_text}\n\n'
                                        f'Чтобы добавить ещё деталь скопируйте номер из каталога'
                                        f' и отправьте в ответ\n{link}',
                                        disable_web_page_preview=True,
                                        reply_markup=markup)
        return 'INPUT_PARTS'
    else:
        parts_list = [f'{number} - {name}' for number, name in context.user_data['car_parts'].items()]
        parts_list_text = '\n'.join(parts_list)
        markup = InlineKeyboardMarkup(save_parts_keyboard)
        context.user_data['markup'] = markup
        await update.message.reply_text(f'Деталь № {part_number} не найдена!\n\n'
                                        f'{parts_list_text}\n\n'
                                        f'Чтобы добавить ещё деталь скопируйте номер из каталога'
                                        f' и отправьте в ответ\n{link}',
                                        disable_web_page_preview=True,
                                        reply_markup=markup)
        return 'INPUT_PARTS'
