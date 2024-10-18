import logging

from aiogram import Bot
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
    date_format = '%Y-%m-%d %H:%M:%S'
    current_date = datetime.now().strftime(date_format)
    for order in orders:
        if order.feedback == 'create':
            delta_time = (datetime.strptime(current_date, date_format) - datetime.strptime(order.datetime_order, date_format))
            if delta_time.days > 0:
                try:
                    await bot.send_message(chat_id=order.tg_id,
                                           text='Пришлите отзыв')
                except:
                    pass
                print(order.tg_id)


if __name__ == "__main__":
    asyncio.run(scheduler_feedback())
