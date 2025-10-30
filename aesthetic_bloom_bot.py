import asyncio
import logging
from pydoc import html
import random
import sys
from os import getenv
from dotenv import load_dotenv
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
from aiogram import F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

load_dotenv()

TOKEN = getenv("BOT_TOKEN")
API_KEY = getenv("PEXELS_API_KEY")

print("BOT_TOKEN:", TOKEN)
print("PEXELS_API_KEY:", API_KEY)

dp = Dispatcher()
user_stats = {}

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    user_name = message.from_user.full_name
    
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🌅 Nature"), KeyboardButton(text="🐱 Animals")],
            [KeyboardButton(text="🚗 Cars"), KeyboardButton(text="🍔 Food")],
            [KeyboardButton(text="🏠 Architecture"), KeyboardButton(text="👨‍💻 Technology")],
            [KeyboardButton(text="🎲 Tasodifiy"), KeyboardButton(text="ℹ️ Yordam")]
        ],
        resize_keyboard=True,
        input_field_placeholder="So'z yozing yoki tugmalardan birini bosing"
    )
    
    text = (
        f"👋 Salom, {html.escape(user_name)}!\n\n"
        "🖼️ <b>Rasm Qidiruv Botiga xush kelibsiz!</b>\n\n"
        "📸 Men sizga turli mavzulardagi sifatli rasmlarni topib beraman.\n\n"
        "🔍 <b>Qanday foydalanish:</b>\n"
        "• Istalgan so'z yozing (masalan: <code>sunset</code>)\n"
        "• Pastdagi kategoriya tugmalaridan foydalaning\n"
        "• Yoki <code>/commands</code> yozib barcha buyruqlarni ko'ring\n\n"
        "🚀 Hozir sinab ko'ring!"
    )

    await message.answer(text, reply_markup=keyboard)

@dp.message(Command("commands"))
@dp.message(Command("help"))
async def show_commands_handler(message: Message):
    commands_text = (
        "🤖 <b>Bot Commandlari:</b>\n\n"
        
        "🔹 <b>/start</b> - Botni ishga tushirish va asosiy menyu\n"
        "🔹 <b>/help</b> - Yordam va commandlar ro'yxati\n"
        "🔹 <b>/commands</b> - Barcha commandlar ro'yxati\n"
        "🔹 <b>/search</b> - Rasm qidirishni boshlash\n"
        "🔹 <b>/random</b> - Tasodifiy rasm olish\n"
        "🔹 <b>/stats</b> - Shaxsiy statistika\n"
        "🔹 <b>/settings</b> - Sozlamalar\n\n"
        
        "📝 <b>Qo'llash usuli:</b>\n"
        "• Istalgan so'z yozing (masalan: <code>cats</code>)\n"
        "• Kategoriya tugmalaridan foydalaning\n"
        "• Commandlardan birini tanlang\n\n"
        
        "🖼️ <i>Masalan: </i><code>nature</code> <i>yozing yoki </i><code>/random</code> <i>commandini ishlating</i>"
    )
    
    await message.answer(commands_text)

@dp.message(Command("search"))
async def command_search_handler(message: Message):
    search_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🔍 Qidirishni boshlash", switch_inline_query_current_chat="")
            ],
            [
                InlineKeyboardButton(text="🌅 Nature", callback_data="search_nature"),
                InlineKeyboardButton(text="🐱 Animals", callback_data="search_animals")
            ],
            [
                InlineKeyboardButton(text="🚗 Transport", callback_data="search_cars"),
                InlineKeyboardButton(text="🍔 Food", callback_data="search_food")
            ]
        ]
    )
    
    search_text = (
        "🔍 <b>Rasm qidirish</b>\n\n"
        "Quyidagi usullardan birini tanlang:\n"
        "• <b>Inline tugma</b> - hozir qidirishni boshlash\n"
        "• <b>Kategoriyalar</b> - tayyor mavzular\n"
        "• <b>Yozish</b> - istalgan so'zni to'g'ridan-to'g'ri yozing\n\n"
        "<i>Masalan: </i><code>ocean sunset</code> <i>yoki </i><code>mountain landscape</code>"
    )
    
    await message.answer(search_text, reply_markup=search_keyboard)

@dp.message(Command("random"))
async def command_random_handler(message: Message):
    random_topics = ["nature", "city", "animal", "food", "travel", "art", "sport", "music", "beach", "mountain"]
    topic = random.choice(random_topics)
    
    await message.answer(f"🎲 Tasodifiy mavzu: <b>{topic}</b>")
    await search_pexels_images(message, topic)

@dp.message(Command("stats"))
async def command_stats_handler(message: Message):
    user_id = message.from_user.id
    stats = user_stats.get(user_id, {"searches": 0, "photos_viewed": 0})
    
    stats_text = (
        f"📊 <b>Sizning statistikangiz:</b>\n\n"
        f"🔍 Qidiruvlar soni: {stats['searches']}\n"
        f"🖼️ Ko'rilgan rasmlar: {stats['photos_viewed']}\n"
        f"👤 Foydalanuvchi ID: {user_id}\n\n"
        f"⭐ Davom eting - ko'proq rasmlar toping!"
    )
    await message.answer(stats_text)

@dp.message(Command("settings"))
async def command_settings_handler(message: Message):
    settings_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="📷 Rasm sifatini o'zgartirish", callback_data="quality_setting"),
                InlineKeyboardButton(text="🔢 Rasm sonini o'zgartirish", callback_data="count_setting")
            ]
        ]
    )
    
    settings_text = (
        "⚙️ <b>Sozlamalar</b>\n\n"
        "Hozircha sozlamalar ishlab chiqilmoqda...\n"
        "Tez orada yangi imkoniyatlar qo'shiladi!"
    )
    
    await message.answer(settings_text, reply_markup=settings_keyboard)

# ========== BUTTON HANDLERS ==========

@dp.message(F.text.in_(["🌅 Nature", "🐱 Animals", "🚗 Cars", "🍔 Food", "🏠 Architecture", "👨‍💻 Technology", "🎲 Tasodifiy", "ℹ️ Yordam"]))
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

@dp.callback_query(F.data.startswith("search_"))
async def handle_search_categories(callback: types.CallbackQuery):
    search_map = {
        "search_nature": "beautiful nature",
        "search_animals": "cute animals", 
        "search_cars": "luxury cars",
        "search_food": "delicious food"
    }
    
    query = search_map[callback.data]
    await callback.message.delete()
    await search_pexels_images(callback.message, query)
    await callback.answer()

@dp.callback_query(F.data.startswith("new_"))
async def handle_new_image(callback: types.CallbackQuery):
    query = callback.data.replace("new_", "")
    await callback.message.delete()
    await search_pexels_images(callback.message, query)
    await callback.answer("🔄 Yangi rasm yuklanmoqda...")

@dp.callback_query(F.data.startswith("like_"))
async def handle_like(callback: types.CallbackQuery):
    await callback.answer("❤️ Sizga rasm yoqdi!", show_alert=False)

# ========== SEARCH FUNCTION ==========

async def search_pexels_images(message: types.Message, query: str):
    try:
        user_id = message.from_user.id
        
        # Statistikani yangilash
        if user_id not in user_stats:
            user_stats[user_id] = {"searches": 0, "photos_viewed": 0}
        user_stats[user_id]["searches"] += 1
        
        page = random.randint(1, 10)
        url = f"https://api.pexels.com/v1/search?query={query}&per_page=5&page={page}"
        headers = {"Authorization": API_KEY}

        response = requests.get(url, headers=headers)
        data = response.json()

        if "photos" not in data or len(data["photos"]) == 0:
            await message.answer("😔 Hech qanday rasm topilmadi\n\nBoshqa so'z yoki kategoriyani sinab ko'ring")
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
            await message.answer_photo(
                photo=photo["src"]["large"],
                caption=caption,
                reply_markup=inline_keyboard
            )
            
    except Exception as e:
        logging.error(f"Search error: {e}")
        await message.answer("❌ Xatolik yuz berdi. Iltimos, keyinroq urinib ko'ring")

# ========== TEXT HANDLER ==========

@dp.message(F.text)
async def search_images(message: types.Message):
    query = message.text.strip()
    
    # Agar command bo'lsa, boshqa handlerlar qabul qilsin
    if query.startswith('/'):
        return
        
    if len(query) < 2:
        await message.answer("❌ Iltimos, kamida 2 ta belgidan iborat so'z kiriting")
        return
        
    if len(query) > 50:
        await message.answer("❌ So'z juda uzun. Iltimos, qisqaroq so'z kiriting")
        return
        
    await message.answer(f"🔍 Qidirilmoqda: <b>{query}</b>")
    await search_pexels_images(message, query)

# ========== MAIN ==========

async def main() -> None:
    print("Bot ishga tushdi 🚀")
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())