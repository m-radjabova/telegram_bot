from aiogram import Router, types, F
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from config import channels
from main import bot 

router = Router()

async def check_sub_channels(user_id):
    result = True
    for channel in channels:
        chat_member = await bot.get_chat_member(chat_id=channel, user_id=user_id)
        if chat_member.status == "left":
            result = False
    return result


@router.callback_query(F.data == "check_subs")
async def check_subs_callback(callback: CallbackQuery):
    if await check_sub_channels(callback.from_user.id):
        await callback.message.edit_text("✅ Rahmat! Siz barcha kanallarga obuna bo‘ldingiz.")
    else:
        await callback.answer("❌ Siz hali barcha kanallarga a'zo bo‘lmagansiz!", show_alert=True)


@router.message(CommandStart())
async def command_start_handler(message: types.Message):
    user_name = message.from_user.full_name

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📚 Lug‘atdan so‘rash", callback_data="search_word")],
            [InlineKeyboardButton(text="📢 Obunani tekshirish", callback_data="check_subs")]
        ]
    )

    await message.answer(
        f"Salom, <b>{user_name}</b>!\n\n"
        "🔹 Pastdagi tugmalardan birini tanlang yoki inglizcha so‘z yuboring:",
        reply_markup=kb
    )
