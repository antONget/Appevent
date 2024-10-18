from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.filters import CommandStart, StateFilter, or_f
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from config_data.config import Config, load_config
import database.requests as rq
import keyboards.keyboard_user as kb
from utils.admin_utils import send_admins

import logging
import asyncio
import random

router = Router()
config: Config = load_config()


class User(StatesGroup):
    number_order = State()
    feed_back = State()


@router.message(CommandStart())
async def process_start_command(message: Message, state: FSMContext) -> None:
    """
    Запуск бота - нажата кнопка "Начать" или введена команда "/start"
    :param message:
    :param state:
    :return:
    """
    logging.info(f"process_start_command {message.chat.id}")
    await state.set_state(state=None)
    if not message.from_user.username:
        username = 'None'
    else:
        username = message.from_user.username
    await rq.add_user(tg_id=message.chat.id,
                      data={"tg_id": message.chat.id, "username": username})
    admins = config.tg_bot.admin_ids.split(',')
    if str(message.chat.id) in admins:
        await message.answer(text=f'Что может этот бот\n\n'
                                  f'Вы администратор проекта.\n'
                                  f'Вы можете изменить коды доступа для объетов',
                             reply_markup=kb.keyboard_start_admin())
    else:
        await message.answer(text=f'Что может этот бот\n\n'
                                  f'',
                             reply_markup=kb.keyboard_start_user())


@router.message(F.text == 'Поддержка')
async def process_support(message: Message, state: FSMContext):
    """
    Выбор ПОДДЕРЖКА
    :param message:
    :param state:
    :return:
    """
    logging.info(f"process_support {message.chat.id}")
    await message.answer(text='Ответы на часто возникающие вопросы вы можете получить в'
                              ' соответствующих разделах или задать их в поддержку',
                         reply_markup=kb.keyboard_question())


@router.callback_query(F.data.startswith('question'))
async def get_answer(callback: CallbackQuery):
    """
    Получаем ответ на вопрос
    :param callback:
    :return:
    """
    answer = callback.data.split('_')[1]
    if answer == '1':
        await callback.message.answer(text='Все инструкции сопровождаются текстом и фото/видео 1')
    elif answer == '2':
        await callback.message.answer(text='Все инструкции сопровождаются текстом и фото/видео 2')
    elif answer == '3':
        await callback.message.answer(text='Все инструкции сопровождаются текстом и фото/видео 3')
    elif answer == '4':
        await callback.message.answer(text='Все инструкции сопровождаются текстом и фото/видео 4')
    await asyncio.sleep(2)
    await callback.message.answer(text=f'Если у вас остались вопросы или предложения, то напишите менеджеру'
                                       f' {config.tg_bot.support_username}')


@router.message(F.text == 'Получить код доступа')
async def process_get_password(message: Message, state: FSMContext):
    """
    Выбор действия пользователем
    :param message:
    :param state:
    :return:
    """
    logging.info(f"process_get_password {message.chat.id}")
    await message.answer(text='Пришлите номер бронирования')
    await state.set_state(User.number_order)


@router.message(F.text, StateFilter(User.number_order))
async def get_number_order(message: Message, state: FSMContext, bot: Bot) -> None:
    """
    Получаем от пользователя имя
    :param message:
    :param state:
    :param bot:
    :return:
    """
    logging.info(f'get_number_order {message.chat.id}')
    number_order = message.text
    order = await rq.get_order_number(number_order=number_order)
    if order:
        title_object = order.title_object
        object_order = await rq.get_object_title(title=title_object)
        if object_order:
            await message.answer(text=f"Здравствуйте, {order.name_client}\n"
                                      f"Вы забронировали {title_object}\n"
                                      f"Дата брони: {order.date_order} {order.month_order}\n"
                                      f"Время брони: {order.time_order}\n\n"
                                      f"Код доступа на объект: {object_order.password_object}")
            await message.answer_video(video=object_order.video_object,
                                       caption='Инструкция как добраться до объекта')
            user_info = await rq.get_user(tg_id=message.chat.id)
            order_user = user_info.list_order.split(',')
            order_user.append(str(order.id))
            await rq.set_order_user(tg_id=message.chat.id, orders=','.join(order_user))
            await rq.set_order_tg_id(tg_id=message.chat.id, id_order=order.id)
        else:
            await message.answer(text='Номер заказа в базе не найден, проверьте введенные данные и'
                                      ' повторите ввод или обратитесь в поддержку')
            await send_admins(bot=bot, text=f'Объект {title_object} в БД отсутствует')
        await state.set_state(state=None)
    else:
        await message.answer(text='Номер заказа в базе не найден, проверьте введенные данные и'
                                  ' повторите ввод или обратитесь в поддержку')
        await state.set_state(state=None)


@router.message(F.text == 'Отзывы')
async def process_feedback(message: Message, state: FSMContext):
    """
    Выбор ОТЗЫВЫ
    :param message:
    :param state:
    :return:
    """
    logging.info(f"process_feedback {message.chat.id}")
    await message.answer(text='Здесь вы можете посмотреть отзывы или оставить отзыв',
                         reply_markup=kb.keyboard_feedback())


@router.callback_query(F.data == 'show_feedback')
async def show_feedback(callback: CallbackQuery):
    """
    Показываем отзывы
    :param callback:
    :return:
    """
    logging.info(f"show_feedback {callback.message.chat.id}")
    await callback.message.answer(text=f'Ссылка на ресурс с отзывами или вывод скриншотов с ними (на обсуждение)')


@router.callback_query(F.data == 'leave_feedback')
async def leave_feedback(callback: CallbackQuery, state: FSMContext):
    """
    Показываем отзывы
    :param callback:
    :return:
    """
    logging.info(f"leave_feedback {callback.message.chat.id}")
    await callback.message.answer(text=f'Пришлите ваш отзыв, нам очень важно ваше мнение')
    await state.set_state(User.feed_back)


@router.message(StateFilter(User.feed_back), or_f(F.document, F.photo, F.video))
async def get_feed_back(message: Message, state: FSMContext):
    """
    Получаем от пользователя контент для отзыва
    :param message:
    :param state:
    :return:
    """
    logging.info(f'get_feed_back {message.chat.id}')
    await asyncio.sleep(random.random())
    data = await state.get_data()
    list_content = data.get('content', [])
    count = data.get('count', [])
    if message.text:
        await message.answer(text=f'📎 Прикрепите фото (можно несколько), видео или документ.')
        return
    elif message.photo:
        content = message.photo[-1].file_id
        if message.caption:
            caption = message.caption
        else:
            caption = 'None'
        await state.update_data(caption=caption)

    elif message.video:
        content = message.video.file_id
        if message.caption:
            caption = message.caption
        else:
            caption = 'None'
        await state.update_data(caption=caption)

    elif message.document:
        content = message.document.file_id
        if message.caption:
            caption = message.caption
        else:
            caption = 'None'
        await state.update_data(caption=caption)

    list_content.append(content)
    count.append(content)
    await state.update_data(content=list_content)
    await state.update_data(count=count)
    await state.set_state(state=None)
    if len(count) == 1:
        await message.answer(text='Добавить еще материал или отправить?',
                             reply_markup=kb.keyboard_send())


@router.callback_query(F.data.endswith('content'))
async def send_add_content(callback: CallbackQuery, state: FSMContext, bot: Bot):
    logging.info(f'send_add_content {callback.message.chat.id}')
    answer = callback.data.split('_')[0]
    if answer == 'add':
        await state.set_state(User.content_state)
        await state.update_data(count=[])
        await callback.message.edit_text(text='📎 Прикрепите фото (можно несколько), видео или документ.')
    else:
        await callback.message.edit_text(text='Материалы от вас переданы\n\n'
                                              'Спасибо! С вами свяжутся',
                                         reply_markup=None)

        data = await state.get_data()
        content = data['content']

        for admin in config.tg_bot.admin_ids.split(','):
            try:
                for item in content:
                    try:
                        await bot.send_photo(chat_id=admin,
                                             photo=item)
                    except:
                        try:
                            await bot.send_video(chat_id=admin,
                                                 video=item)
                        except:
                            await bot.send_document(chat_id=admin,
                                                    document=item)
            except:
                await bot.send_message(chat_id=admin,
                                       text='Не удалось отправить контент')
        await state.set_state(state=None)

