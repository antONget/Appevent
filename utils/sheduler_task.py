import logging

from aiogram import Bot
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from database import requests as rq
from datetime import datetime, date
import asyncio


async def scheduler_feedback(bot: Bot):
    """
    Планировщик задач для оставления отзыва через сутки после посещения зала
    :return:
    """
    logging.info(f'scheduler_feedback')
    orders = await rq.get_orders()
    date_format = '%d/%m/%Y %H:%M:%S'
    current_date = datetime.now().strftime(date_format)
    for order in orders:
        if order.feedback == 'create':
            delta_time = (datetime.strptime(current_date, date_format) - datetime.strptime(order.datetime_order, date_format))
            if delta_time.days > 0:
                try:
                    button_1 = InlineKeyboardButton(text='Оставить отзыв', callback_data=f'leave_feedback')
                    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_1]], )
                    await bot.send_message(chat_id=order.tg_id,
                                           text='Пришлите отзыв',
                                           reply_markup=keyboard)
                    await rq.set_order_feedback(id_order=order.id)
                except:
                    pass


async def scheduler_remember(bot: Bot):
    """
    Планировщик задач для оставления отзыва через сутки после посещения зала
    :return:
    """
    logging.info(f'scheduler_feedback')
    orders = await rq.get_orders()
    date_format = '%d/%m/%Y %H:%M:%S'
    current_date = datetime.now().strftime(date_format)
    for order in orders:
        if order.feedback == 'create':
            delta_time = (datetime.strptime(order.datetime_order, date_format) - datetime.strptime(current_date, date_format))
            if delta_time.days < 0:
                try:
                    await bot.send_message(chat_id=order.tg_id,
                                           text=f'Привет!\n'
                                                f'Напоминаем, что ты забронировал(а):\n'
                                                f'Зал: {order.title_object}.\n'
                                                f'Дата {order.date_order} {order.month_order}\n'
                                                f'Время начала:{order.time_order}\n'
                                                f'Время конца: {order.finish_date_order.split()[-1]}\n\n'
                                                f'<b>Не забудь получить код-доступа и отправить'
                                                f' его клиентам вместе с памяткой!</b>\n'
                                                f'Ждем тебя🤩')
                    await rq.set_order_feedback(id_order=order.id)
                except:
                    pass


if __name__ == "__main__":
    asyncio.run(scheduler_feedback())
