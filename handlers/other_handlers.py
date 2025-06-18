import asyncio

from aiogram import Router, Bot, F
from aiogram.types import Message, CallbackQuery
from aiogram.types import FSInputFile
from database import requests as rq
from config_data.config import Config, load_config
from datetime import date, datetime
from database.requests import add_order, get_order_number
import logging

router = Router()
config: Config = load_config()


@router.callback_query()
async def all_callback(callback: CallbackQuery) -> None:
    logging.info(f'all_callback: {callback.message.chat.id} / {callback.data}')
    await callback.message.answer(text='Я вас не понимаю!')
    await callback.answer()


@router.message(F.text)
async def all_message(message: Message, bot: Bot) -> None:
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

    elif message.chat.id == -1002503953563:
        content = message.text.split('\n')
        if not content[0] == 'Поступила оплата!':
            return
        data = {}
        for row in content:
            if "Бронь №" in row:
                number_order = int(row.split('№')[-1])
                result = await get_order_number(number_order=number_order)
                if result:
                    await bot.send_message(chat_id=-1002503953563,
                                           text=f'Заказ №{number_order} уже размещен в базе данных')
                    return
                else:
                    await bot.send_message(chat_id=-1002503953563,
                                           text=f'Заказ №{number_order} в БД не найден. Производим его размещение')
                data["number_order"] = number_order
            elif "Начнется:" in row:
                dict_month = {'января': '01', 'февраля': '02', 'марта': '03',
                              'апреля': '04', 'мая': '05', 'июня': '06',
                              'июля': '07', 'августа': '08', 'сентября': '09',
                              'октября': '10', 'ноября': '11', 'декабря': '12'}
                print(row)
                date_order = row.split()[1]
                data["date_order"] = date_order
                month_order = row.split()[2].replace(',', '')
                data["month_order"] = month_order
                time_order = row.split()[4].replace(',', '')
                data["time_order"] = time_order
                long_order = row.split()[6]
                data["long_order"] = long_order
                current_date = date.today()
                datetime_order = datetime(year=current_date.year,
                                                   month=int(dict_month[month_order]),
                                                   day=int(date_order),
                                                   hour=int(time_order.split(':')[0]),
                                                   minute=0).strftime("%d/%m/%Y %H:%M:%S")
                data["datetime_order"] = datetime_order
            elif "Зал:" in row:
                title_object = row.split(maxsplit=1)[-1][:-1]
                data["title_object"] = title_object
            elif "Имя:" in row:
                name_client = ' '.join(row.split()[1:])
                data["name_client"] = name_client
            elif "Телефон:" in row:
                phone_client = row.split()[1].replace('.', '')
                data["phone_client"] = phone_client
            elif "Email:" in row:
                email_client = row.split()[1].replace('.', '')
                data["email_client"] = email_client
            elif "Закончится:" in row:
                finish_date_order = row.split(maxsplit=1)[1]
                data["finish_date_order"] = finish_date_order
            # data = {"number_order": number_order,
            #         "date_order": date_order,
            #         "month_order": month_order,
            #         "time_order": time_order,
            #         "long_order": long_order,
            #         "title_object": title_object,
            #         "name_client": name_client,
            #         "phone_client": phone_client,
            #         "email_client": email_client,
            #         "datetime_order": datetime_order}
        await add_order(data=data)
    else:
        await message.answer('Я вас не понимаю!')
