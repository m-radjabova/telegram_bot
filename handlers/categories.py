from aiogram import Router, types, F
import random
from handlers.commands import show_commands_handler
from services.pexels_api import search_pexels_images

router = Router()

@router.message(F.text.in_(["🌅 Nature", "🐱 Animals", "🚗 Cars", "🍔 Food", "🏠 Architecture", "👨‍💻 Technology", "🎲 Tasodifiy", "ℹ️ Yordam"]))
async def handle_category_buttons(message: types.Message):
    if message.text == "ℹ️ Yordam":
        await show_commands_handler(message)
        return

    category_map = {
        "🌅 Nature": "beautiful nature landscape",
        "🐱 Animals": "cute animals pets",
        "🚗 Cars": "sports cars luxury",
        "🍔 Food": "delicious food cooking",
        "🏠 Architecture": "modern architecture building",
        "👨‍💻 Technology": "technology gadgets",
        "🎲 Tasodifiy": random.choice(["nature", "city", "animal", "food", "travel"])
    }

    query = category_map[message.text]
    await message.answer(f"🔍 Qidirilmoqda: <b>{query}</b>")
    await search_pexels_images(message, query)
