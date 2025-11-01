import logging
import random
import requests
from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import PEXELS_API_KEY

user_stats = {}

async def search_pexels_images(message: types.Message, query: str):
    try:
        user_id = message.from_user.id

        if user_id not in user_stats:
            user_stats[user_id] = {"searches": 0, "photos_viewed": 0}
        user_stats[user_id]["searches"] += 1

        page = random.randint(1, 10)
        url = f"https://api.pexels.com/v1/search?query={query}&per_page=5&page={page}"
        headers = {"Authorization": PEXELS_API_KEY}

        response = requests.get(url, headers=headers)
        data = response.json()

        if "photos" not in data or len(data["photos"]) == 0:
            await message.answer("😔 Hech qanday rasm topilmadi")
            return

        photos = data["photos"]
        random.shuffle(photos)

        for photo in photos[:5]:
            user_stats[user_id]["photos_viewed"] += 1
            inline_keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(text="📷 Fotograf", url=photo["photographer_url"]),
                        InlineKeyboardButton(text="🔗 Asl rasm", url=photo["url"])
                    ],
                    [
                        InlineKeyboardButton(text="🔄 Yangi rasm", callback_data=f"new_{query}"),
                        InlineKeyboardButton(text="❤️ Like", callback_data=f"like_{photo['id']}")
                    ]
                ]
            )

            caption = f"📸 <b>Fotograf:</b> {photo['photographer']}\n📏 <b>O'lcham:</b> {photo['width']}x{photo['height']}"
            await message.answer_photo(photo=photo["src"]["large"], caption=caption, reply_markup=inline_keyboard)

    except Exception as e:
        logging.error(f"Search error: {e}")
        await message.answer("❌ Xatolik yuz berdi.")
