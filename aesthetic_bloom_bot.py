import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN

from handlers import start, ish_joy_kerak, xodim_kerak

async def main():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    dp.include_router(start.router)
    dp.include_router(ish_joy_kerak.router)
    dp.include_router(xodim_kerak.router)

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())