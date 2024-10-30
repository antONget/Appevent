from database.models import User, Order, Object
from database.models import async_session
from sqlalchemy import select, update, delete
from dataclasses import dataclass
import logging


"""USER"""


async def add_user(tg_id: int, data: dict) -> None:
    """
    Добавляем нового пользователя если его еще нет в БД
    :param tg_id:
    :param data:
    :return:
    """
    logging.info(f'add_user')
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        # если пользователя нет в базе
        if not user:
            session.add(User(**data))
            await session.commit()


async def get_user(tg_id: int) -> User:
    """
    Возвращаем запись о пользователе по его id
    :param tg_id:
    :return:
    """
    logging.info(f'get_user')
    async with async_session() as session:
        return await session.scalar(select(User).where(User.tg_id == tg_id))


async def set_order_user(tg_id: int, orders: str) -> None:
    """
    Обновляем у пользователя список заказов
    :param tg_id:
    :param orders:
    :return:
    """
    logging.info(f'set_order_user')
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if user:
            user.list_order = orders
            await session.commit()


""" ORDER """


async def add_order(data: dict) -> None:
    """
    Добавляем заявку
    :param data:
    :return:
    """
    logging.info(f'add_order')
    async with async_session() as session:
        order = Order(**data)
        session.add(order)
        await session.commit()


async def get_order_number(number_order: int) -> Order:
    """
    Возвращаем запись о заказе по его номеру
    :param number_order:
    :return:
    """
    logging.info(f'get_order_number')
    async with async_session() as session:
        return await session.query(Order).filter(Order.number_order == number_order)


async def get_orders() -> Order:
    """
    Возвращаем записи о заказах
    :return:
    """
    logging.info(f'get_orders')
    async with async_session() as session:
        return await session.scalars(select(Order))


async def set_order_tg_id(tg_id: int, id_order: int) -> None:
    """
    Возвращаем запись об объекте по его id
    :param tg_id:
    :param id_order:
    :return:
    """
    logging.info(f'set_order_tg_id')
    async with async_session() as session:
        order = await session.scalar(select(Order).where(Order.id == id_order))
        if order:
            order.tg_id = tg_id
            await session.commit()


async def set_order_feedback(id_order: int) -> None:
    """
    Возвращаем запись об объекте по его id
    :param tg_id:
    :param id_order:
    :return:
    """
    logging.info(f'set_order_tg_id')
    async with async_session() as session:
        order = await session.scalar(select(Order).where(Order.id == id_order))
        if order:
            order.feedback = 'remember'
            await session.commit()


""" OBJECT """


async def get_object_title(title: str) -> Object:
    """
    Возвращаем запись об объекте по его названию
    :param title:
    :return:
    """
    logging.info(f'get_object_title')
    async with async_session() as session:
        return await session.scalar(select(Object).where(Object.title_object == title))


async def get_objects() -> Object:
    """
    Возвращаем записи об объектах
    :return:
    """
    logging.info(f'get_object_title')
    async with async_session() as session:
        return await session.scalars(select(Object).order_by(Object.id))


async def get_object_id(id_: int) -> Object:
    """
    Возвращаем запись об объекте по его id
    :param id_:
    :return:
    """
    logging.info(f'get_object_title')
    async with async_session() as session:
        return await session.scalar(select(Object).where(Object.id == id_))


async def set_object_id(id_: int, password: str) -> None:
    """
    Возвращаем запись об объекте по его id
    :param id_:
    :param password:
    :return:
    """
    logging.info(f'get_object_title')
    async with async_session() as session:
        object_ = await session.scalar(select(Object).where(Object.id == id_))
        if object_:
            object_.password_object = password
            await session.commit()