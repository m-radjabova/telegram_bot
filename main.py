import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from config import BOT_TOKEN
from filter.channel_midleware import SubscriptionMiddleware
from handlers import start, qarz, qarz_view, qarz_debt

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

async def main():
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)

    dp.include_router(start.router)
    dp.include_router(qarz.router)
    dp.include_router(qarz_view.router)
    dp.include_router(qarz_debt.router)

    
    dp.message.middleware(SubscriptionMiddleware())
    dp.callback_query.middleware(SubscriptionMiddleware())


    print("🚀 Bot ishga tushdi...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
