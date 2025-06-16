import asyncio
import os

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from scheduler import start_scheduler

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")


async def main():
    dp = Dispatcher()
    start_scheduler()
    await dp.start_polling(Bot(token=BOT_TOKEN))


if __name__ == "__main__":
    asyncio.run(main())
