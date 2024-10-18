from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from database.models import User
import logging


def keyboard_password() -> InlineKeyboardMarkup:
    logging.info("keyboard_send")
    button_1 = InlineKeyboardButton(text='Получить коды доступа', callback_data=f'get_password')
    button_2 = InlineKeyboardButton(text='Изменить коды доступа', callback_data=f'update_password')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_1], [button_2]],)
    return keyboard

