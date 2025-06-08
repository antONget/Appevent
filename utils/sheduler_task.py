import logging

from aiogram import Bot
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from database import requests as rq
from database.models import Order
from datetime import datetime, timedelta
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
        if order.feedback == 'remember':
            delta_time = (datetime.strptime(current_date, date_format) -
                          datetime.strptime(order.datetime_order, date_format) + timedelta(days=1))
            # если время заказа прошло
            if delta_time.days > 0:
                try:
                    button_1 = InlineKeyboardButton(text='Оставить отзыв', callback_data=f'leave_feedback')
                    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_1]], )
                    await bot.send_message(chat_id=order.tg_id,
                                           text='Привет!\n'
                                                'Тебе у нас понравилось?😻\n\n'
                                                'Пожалуйста, оставь отзыв! А мы дадим тебе промокод на 20%'
                                                ' на следующее занятие 😎\n\n'
                                                'Наши социальные сети:\n'
                                                '📱<a href="https://yandex.ru/maps/-/CHfYVZNS">Яндекс.Карты</a>\n'
                                                '📍<a href="">2ГИС</a>\n'
                                                '📱Google.Карты\n'
                                                '📱<a href="https://www.instagram.com/tvoiystart">Instagram</a>\n'
                                                '📱<a href="https://vk.com/tvoiystart">VK</a>\n'
                                                '📱<a href="https://t.me/tvoiystart">Telegram</a>',
                                           reply_markup=keyboard)
                    await rq.set_order_feedback(id_order=order.id, feedback='feedback')
                except:
                    pass


async def scheduler_remember(bot: Bot):
    """
    Планировщик задач для оставления отзыва через сутки после посещения зала
    :return:
    """
    logging.info(f'scheduler_remember')
    orders: list[Order] = await rq.get_orders()
    date_format = '%d/%m/%Y %H:%M:%S'
    current_date = datetime.now().strftime(date_format)
    for order in orders:
        if order.feedback == 'create':
            delta_time = (datetime.strptime(order.datetime_order, date_format) -
                          datetime.strptime(current_date, date_format) - timedelta(hours=2))
            # если время заказа не наступило
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
                    await rq.set_order_feedback(id_order=order.id, feedback='remember')
                except:
                    pass


if __name__ == "__main__":
    asyncio.run(scheduler_feedback())
