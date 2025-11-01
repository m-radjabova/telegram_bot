from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
import random
from services.pexels_api import search_pexels_images, user_stats

router = Router()

@router.message(Command("commands"))
@router.message(Command("help"))
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

@router.message(Command("search"))
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
        "• <b>Yozish</b> - istalgan so'zni yozing"
    )
    await message.answer(search_text, reply_markup=search_keyboard)

@router.message(Command("random"))
async def command_random_handler(message: Message):
    random_topics = ["nature", "city", "animal", "food", "travel", "art", "sport", "music", "beach", "mountain"]
    topic = random.choice(random_topics)
    await message.answer(f"🎲 Tasodifiy mavzu: <b>{topic}</b>")
    await search_pexels_images(message, topic)

@router.message(Command("stats"))
async def command_stats_handler(message: Message):
    user_id = message.from_user.id
    stats = user_stats.get(user_id, {"searches": 0, "photos_viewed": 0})
    stats_text = (
        f"📊 <b>Sizning statistikangiz:</b>\n\n"
        f"🔍 Qidiruvlar soni: {stats['searches']}\n"
        f"🖼️ Ko'rilgan rasmlar: {stats['photos_viewed']}\n"
        f"👤 Foydalanuvchi ID: {user_id}"
    )
    await message.answer(stats_text)

@router.message(Command("settings"))
async def command_settings_handler(message: Message):
    settings_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[
            InlineKeyboardButton(text="📷 Rasm sifatini o'zgartirish", callback_data="quality_setting"),
            InlineKeyboardButton(text="🔢 Rasm sonini o'zgartirish", callback_data="count_setting")
        ]]
    )

    settings_text = (
        "⚙️ <b>Sozlamalar</b>\n\n"
        "Hozircha sozlamalar ishlab chiqilmoqda..."
    )
    await message.answer(settings_text, reply_markup=settings_keyboard)
