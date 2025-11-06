from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import channels

def sub_keyboard():
    buttons = []
    for channel in channels:
        buttons.append([InlineKeyboardButton(text=f"📢 {channel} ga a'zo bo'lish", url=f"https://t.me/{channel[1:]}")])
    buttons.append([InlineKeyboardButton(text="✅ Tekshirish", callback_data="check_subs")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)