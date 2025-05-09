import logging

from telethon import TelegramClient, sync, events
from config_data.config import Config, load_config

from database.requests import add_order
from database.models import async_main
from datetime import date
import datetime
config: Config = load_config()

api_id = 27553479
api_hash = 'b97a7c148d46268b14ee49e63dd6511b'
phone = config.tg_bot.phone
login = config.tg_bot.login


bot = TelegramClient('session_name', api_id, api_hash)


@bot.on(events.NewMessage())
async def my_handler(event):
    await async_main()
    logging.info(event.message.chat.id)
    if event.message.chat.id == 7513602824: # 191328935
        content = event.message.text.split('\n')
        if not content[0] == 'Новая заявка с виджета!':
            return
        for row in content:
            if "Заявка №" in row:
                number_order = row.split('№')[-1]
            elif "Начинается:" in row:
                dict_month = {'января': '01', 'февраля': '02', 'марта': '03',
                              'апреля': '04', 'мая': '05', 'июня': '06',
                              'июля': '07', 'августа': '08', 'сентября': '09',
                              'октября': '10', 'ноября': '11', 'декабря': '12'}
                date_order = row.split()[1]
                month_order = row.split()[2].replace(',', '')

                time_order = row.split()[4].replace(',', '')
                long_order = row.split()[6]
                current_date = date.today()
                datetime_order = datetime.datetime(year=current_date.year,
                                                   month=int(dict_month[month_order]),
                                                   day=int(date_order),
                                                   hour=int(time_order.split(':')[0]),
                                                   minute=0)
            elif "Зал:" in row:
                title_object = row.split()[1][:-1]
            elif "Имя:" in row:
                name_client = ' '.join(row.split()[1:])
            elif "Телефон:" in row:
                phone_client = row.split()[1].replace('.', '')
            elif "Email:" in row:
                email_client = row.split()[1].replace('.', '')

        data = {"number_order": number_order,
                "date_order": date_order,
                "month_order": month_order,
                "time_order": time_order,
                "long_order": long_order,
                "title_object": title_object,
                "name_client": name_client,
                "phone_client": phone_client,
                "email_client": email_client,
                "datetime_order": datetime_order}
        await add_order(data=data)

# Запуск клиента
bot.start()
