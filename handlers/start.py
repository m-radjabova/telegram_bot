from aiogram import Router, types
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from pydoc import html

router = Router()

@router.message(CommandStart())
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
