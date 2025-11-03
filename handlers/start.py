from aiogram import Router, Bot
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
from aiogram.filters import CommandStart
from aiogram.utils.markdown import hlink
from config import BOT_TOKEN, CHANNEL_ID

router = Router()
bot = Bot(token=BOT_TOKEN)

@router.message(CommandStart())
async def command_start_handler(message: Message):
    user_id = message.from_user.id
    user_name = message.from_user.full_name

    try:
        member = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)

        if member.status in ["member", "administrator", "creator"]:
            text = f"👋 Salom, {user_name}!\nQuyidagilardan birini tanlang:"

            buttons = [
                [
                    KeyboardButton(text="🏢 Ish joy kerak"),
                    KeyboardButton(text="👷 Xodim kerak")
                ]
            ]
            keyboard = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

            await message.answer(text, reply_markup=keyboard)
        else:
            raise Exception("not_subscribed")

    except Exception as e:
        link = f"https://t.me/{CHANNEL_ID.replace('@','')}"
        await message.answer(
            f"⚠️ Iltimos, 📢 <a href='{link}'>kanalga obuna bo‘ling</a> va qayta /start bosing.",
            parse_mode="HTML"
        )
