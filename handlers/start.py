from aiogram import Router, types, F
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, CallbackQuery
from pydoc import html
from config import channels

from filter.channel_midleware import SubscriptionMiddleware
from main import dp, bot

router = Router()

async def check_sub_channels(user_id):
    result = True
    for channel in channels:
        chat_member = await bot.get_chat_member(chat_id=channel, user_id=user_id)
        if chat_member.status == "left":
            result = False
    return result


@dp.callback_query(F.data == "check_subs")
async def check_subs_callback(callback: CallbackQuery):
    print("jefhijknvhksdv ")
    if await check_sub_channels(callback.from_user.id):
        await callback.message.edit_text("✅ Rahmat! Siz barcha kanallarga obuna bo‘ldingiz.")
    else:
        await callback.answer("❌ Siz hali barcha kanallarga a'zo bo‘lmagansiz!", show_alert=True)


@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    user_name = message.from_user.full_name

    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Qarz Berish"), KeyboardButton(text="Qarzlar ro'yxati")],
            [KeyboardButton(text="Qarzni o'chirish(To'lash)")],
        ],
        resize_keyboard=True,
        input_field_placeholder="So'z yozing yoki tugmalardan birini bosing"
    )

    text = (
        f"👋 Salom, {html.escape(user_name)}!\n\n"
    )

    await message.answer(text, reply_markup=keyboard)