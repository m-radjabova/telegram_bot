from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from config import channels

from keyboard.keyboard import sub_keyboard


class SubscriptionMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        user_id = None
        if isinstance(event, Message):
            user_id = event.from_user.id
        elif isinstance(event, CallbackQuery):
            user_id = event.from_user.id
        
        if user_id:
            for channel in channels:
                chat_member = await data["bot"].get_chat_member(chat_id=channel, user_id=user_id)
                if chat_member.status == "left":
                    # User is not subscribed
                    if isinstance(event, Message):
                        await event.answer(
                            "❗ Botdan foydalanish uchun quyidagi kanallarga obuna bo‘ling:",
                            reply_markup=sub_keyboard()
                        )
                    elif isinstance(event, CallbackQuery):
                        await event.answer("❌ Siz hali barcha kanallarga a'zo bo‘lmagansiz!", show_alert=True)
                    return  # Stop processing further handlers
        
        return await handler(event, data)  # Continue to the handler