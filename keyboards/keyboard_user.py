from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from database.models import User
import logging


def keyboard_start_user() -> ReplyKeyboardMarkup:
    logging.info("keyboard_start")
    button_1 = KeyboardButton(text='Получить код доступа')
    button_2 = KeyboardButton(text='Поддержка')
    button_3 = KeyboardButton(text='Отзывы')
    keyboard = ReplyKeyboardMarkup(keyboard=[[button_1], [button_2], [button_3]])
    return keyboard


def keyboard_start_admin() -> ReplyKeyboardMarkup:
    logging.info("keyboard_start")
    button_1 = KeyboardButton(text='Получить код доступа')
    button_2 = KeyboardButton(text='Поддержка')
    button_3 = KeyboardButton(text='Отзывы')
    button_4 = KeyboardButton(text='Код доступа')
    keyboard = ReplyKeyboardMarkup(keyboard=[[button_1], [button_2], [button_3], [button_4]])
    return keyboard


def keyboard_question() -> InlineKeyboardMarkup:
    logging.info("keyboard_send")
    button_1 = InlineKeyboardButton(text='Как добраться', callback_data=f'question_1')
    button_2 = InlineKeyboardButton(text='Как открыть студию', callback_data=f'question_2')
    button_3 = InlineKeyboardButton(text='Правила нахождения в студии', callback_data=f'question_3')
    button_4 = InlineKeyboardButton(text='Как настроить свет, звук и вентиляцию', callback_data=f'question_4')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_1], [button_2], [button_3], [button_4]],)
    return keyboard


def keyboard_feedback() -> InlineKeyboardMarkup:
    logging.info("keyboard_feedback")
    button_1 = InlineKeyboardButton(text='Посмотреть отзывы', callback_data=f'show_feedback')
    button_2 = InlineKeyboardButton(text='Оставить отзыв', callback_data=f'leave_feedback')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_1], [button_2]],)
    return keyboard


def keyboard_send() -> InlineKeyboardMarkup:
    logging.info("keyboard_send")
    button_1 = InlineKeyboardButton(text='Отправить', callback_data=f'send_content')
    button_2 = InlineKeyboardButton(text='Добавить', callback_data=f'add_content')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_2], [button_1]],)
    return keyboard
