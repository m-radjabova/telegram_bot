# main.py
import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher, types, Router
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from config import BOT_TOKEN, DICTIONARY_API_KEY
from filter.channel_midleware import SubscriptionMiddleware
from services.dictionary_api import DictionaryAPI
from handlers import start 

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

dictionary = DictionaryAPI(DICTIONARY_API_KEY)
router = Router()

# --- Callback (lug‘atdan so‘rash) ---
@router.callback_query(lambda c: c.data == "search_word")
async def ask_word(callback: types.CallbackQuery):
    await callback.message.answer("✍️ Inglizcha so‘z yuboring (masalan: <b>example</b>)")
    await callback.answer()


# --- Tarjima qabul qilish ---
@router.message()
async def translate_word(message: types.Message):
    word = message.text.strip().lower()
    result = dictionary.get_word(word)

    if not result:
        await message.answer("❌ So‘z topilmadi yoki tarjima olishda xato yuz berdi.")
        return

    text = f"📖 <b>{word}</b>\n\n💬 <b>Tarjima:</b> {result}"
    await message.answer(text)


async def main():
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)

    dp.message.middleware(SubscriptionMiddleware())
    dp.callback_query.middleware(SubscriptionMiddleware())

    dp.include_router(start.router)  
    dp.include_router(router)     

    print("🚀 Bot ishga tushdi...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

