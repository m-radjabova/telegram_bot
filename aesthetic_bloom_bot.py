import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command

from config import BOT_TOKEN
from handlers import start, commands, categories, callbacks, search


async def main():
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()

    # 🔹 Register all handlers
    dp.message.register(start.command_start_handler, CommandStart())
    dp.message.register(commands.show_commands_handler, Command("commands"))
    dp.message.register(commands.command_search_handler, Command("search"))
    dp.message.register(commands.command_random_handler, Command("random"))
    dp.message.register(commands.command_stats_handler, Command("stats"))
    dp.message.register(commands.command_settings_handler, Command("settings"))

    dp.message.register(categories.handle_category_buttons)
    dp.callback_query.register(callbacks.handle_search_categories)
    dp.callback_query.register(callbacks.handle_new_image)
    dp.callback_query.register(callbacks.handle_like)
    dp.message.register(search.search_images)

    print("🚀 Bot ishga tushdi")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
