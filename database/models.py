from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from dataclasses import dataclass


engine = create_async_engine(url="sqlite+aiosqlite:///database/db.sqlite3", echo=False)
async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(Integer)
    username: Mapped[str] = mapped_column(String())
    list_order: Mapped[str] = mapped_column(String(),  default='0')


class Order(Base):
    __tablename__ = 'orders'

    id: Mapped[int] = mapped_column(primary_key=True)
    number_order = mapped_column(Integer)
    date_order: Mapped[str] = mapped_column(String(200))
    month_order: Mapped[str] = mapped_column(String(200))
    time_order: Mapped[str] = mapped_column(String(20))
    long_order: Mapped[str] = mapped_column(String(200))
    title_object: Mapped[str] = mapped_column(String(200))
    name_client: Mapped[str] = mapped_column(String(200))
    phone_client: Mapped[str] = mapped_column(String(200))
    email_client: Mapped[str] = mapped_column(String(200))
    datetime_order: Mapped[str] = mapped_column(String(200))
    feedback: Mapped[str] = mapped_column(String(20), default='create')
    tg_id: Mapped[int] = mapped_column(Integer(), default=0)


class Object(Base):
    __tablename__ = 'object'

    id: Mapped[int] = mapped_column(primary_key=True)
    title_object = mapped_column(String(200))
    video_object: Mapped[str] = mapped_column(String(200))
    password_object: Mapped[str] = mapped_column(String(200))


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# import asyncio
#
# asyncio.run(async_main())
