from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.filters import CommandStart, StateFilter, or_f
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from config_data.config import Config, load_config
import database.requests as rq
from database.models import Object
import keyboards.keyboard_admin as kb
from utils.admin_utils import send_admins

import logging
import asyncio
import random

router = Router()
config: Config = load_config()


class Admin(StatesGroup):
    number_order = State()
    feed_back = State()
    number_object = State()
    password_object = State()


@router.message(F.text == 'Код доступа')
async def process_cod_password(message: Message):
    """
    Выбор КОД ДОСТУПА
    :param message:
    :return:
    """
    logging.info(f"process_cod_password {message.chat.id}")
    await message.answer(text='Вы можете просмотреть текущие коды доступа для объектов или изменить их',
                         reply_markup=kb.keyboard_password())


@router.callback_query(F.data == 'get_password')
async def get_password(callback: CallbackQuery, state: FSMContext):
    """
    Получаем коды доступа для объектов
    :param callback:
    :return:
    """
    logging.info(f"get_password {callback.message.chat.id}")
    objects = await rq.get_objects()
    list_objects = [object_ for object_ in objects]
    text = '<b>Коды доступа для объектов:</b>\n\n'
    for obj in list_objects:
        text += f'<i>{obj.id}. {obj.title_object}</i>: {obj.password_object}\n'
    await callback.message.edit_text(text=text)
    await callback.answer()


@router.callback_query(F.data == 'update_password')
async def update_password(callback: CallbackQuery, state: FSMContext):
    """
    Обновление кода доступа
    :param callback:
    :param state:
    :return:
    """
    logging.info(f"get_password {callback.message.chat.id}")
    objects = await rq.get_objects()
    list_objects = [object_ for object_ in objects]
    text = '<b>Коды доступа для объектов:</b>\n\n'
    for obj in list_objects:
        text += f'<i>{obj.id}. {obj.title_object}</i>: {obj.password_object}\n'
    text += '\nПришлите новый код для доступа на объекты'
    await callback.message.edit_text(text=text)
    await state.set_state(Admin.password_object)
    await callback.answer()
#
#
# @router.message(F.text, StateFilter(Admin.number_object))
# async def get_number_object(message: Message, state: FSMContext):
#     """
#     Получение номер объекта
#     :param message:
#     :param state:
#     :return:
#     """
#     logging.info(f"get_number_object {message.chat.id}")
#     if not message.text.isdigit() or int(message.text) <= 0:
#         await message.answer(text='Номер объекта должен быть целым числом')
#         return
#     number_object = int(message.text)
#     object_ = await rq.get_object_id(number_object)
#     if object_:
#         await state.update_data(number_object=number_object)
#         await message.answer(text=f'Пришлите новый код для объекта {object_.title_object}')
#         await state.set_state(Admin.password_object)
#     else:
#         await message.answer(text=f'Объекта с таким номером нет в БД')


@router.message(F.text, StateFilter(Admin.password_object))
async def get_password_object(message: Message, state: FSMContext):
    """
    Получение кода доступа
    :param message:
    :param state:
    :return:
    """
    logging.info(f"get_number_object {message.chat.id}")
    if not message.text.isdigit() or int(message.text) <= 0:
        await message.answer(text='Код должен содержать только числа')
        return
    if len(message.text) != 6:
        await message.answer(text='Код должен содержать 6 цифры')
        return
    password_object = f'{message.text}#'
    await rq.set_object_all(password=password_object)
    await message.answer(text=f'Код обновлен на {message.text}')
    await state.set_state(state=None)
