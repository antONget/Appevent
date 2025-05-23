import asyncio

from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.types import FSInputFile
from database import requests as rq
from config_data.config import Config, load_config

import logging

router = Router()
config: Config = load_config()


@router.callback_query()
async def all_callback(callback: CallbackQuery) -> None:
    logging.info(f'all_callback: {callback.message.chat.id} / {callback.data}')
    await callback.message.answer(text='Я вас не понимаю!')
    await callback.answer()


@router.message()
async def all_message(message: Message) -> None:
    logging.info(f'all_message {message.chat.id} / {message.text}')
    if message.photo:
        logging.info(f'all_message message.photo')
        print(message.photo[-1].file_id)
        return

    if message.video:
        logging.info(f'all_message message.photo')
        print(message.video.file_id)
        return

    if message.document:
        logging.info(f'all_message message.photo')
        print(message.document.file_id)
        return

    if message.sticker:
        logging.info(f'all_message message.sticker')
        return

    # команды доступные администраторам
    # list_super_admin = list(map(int, config.tg_bot.admin_ids.split(',')))
    # if message.chat.id in list_super_admin:
    logging.info(f'all_message message.admin')
    if message.text == '/get_logfile':
        logging.info(f'all_message message.admin./get_logfile')
        file_path = "py_log.log"
        await message.answer_document(FSInputFile(file_path))

    elif message.text == '/get_dbfile':
        logging.info(f'all_message message.admin./get_dbfile')
        file_path = "database/db.sqlite3"
        await message.answer_document(FSInputFile(file_path))

        # elif message.text == '/get_listusers':
        #     logging.info(f'all_message message.admin./get_listusers')
        #     list_user = await get_all_users()
        #     text = 'Список пользователей:\n\n'
        #     for i, user in enumerate(list_user):
        #         text += f'{i+1}. @{user.username}/{user.tg_id}\n'
        #         if i % 10 == 0 and i > 0:
        #             await asyncio.sleep(0.2)
        #             await message.answer(text=text)
        #             text = ''
        #     await message.answer(text=text)

    elif message.text == '/get_countorder':
        orders = await rq.get_orders()
        count_order = len([order for order in orders])
        await message.answer(text=f'Количество заявок - {count_order}')
    else:
        await message.answer('Я вас не понимаю!')
