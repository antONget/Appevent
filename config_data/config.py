from dataclasses import dataclass
from environs import Env


@dataclass
class TgBot:
    api_id: str
    api_hash: str
    phone: str
    login: str
    token: str
    admin_ids: str
    support_id: int
    support_username: str



@dataclass
class Config:
    tg_bot: TgBot


def load_config(path: str = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(tg_bot=TgBot(api_id=env('API_ID'),
                               api_hash=env('API_HASH'),
                               phone=env('PHONE'),
                               login=env('LOGIN'),
                               admin_ids=env('ADMIN_IDS'),
                               token=env('BOT_TOKEN'),
                               support_id=env('SUPPORT_ID'),
                               support_username=env('SUPPORT_USERNAME')
                               ))
