from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.fsm.context import FSMContext

from states.xodim_kerak_state import XodimKerak

router = Router()

ADMIN_ID = 7022476161

@router.message(F.text == "👷 Xodim kerak")
async def xodim_kerak(message: Message, state: FSMContext):
    await message.answer("🎓 Idora nomi?", reply_markup=ReplyKeyboardRemove())
    await state.set_state(XodimKerak.idora)

@router.message(XodimKerak.idora)
async def get_idora(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("📚 Texnologiya:")
    await state.set_state(XodimKerak.texnologiya)

@router.message(XodimKerak.texnologiya)
async def get_idora(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("📞 Aloqa: ")
    await state.set_state(XodimKerak.aloqa)

@router.message(XodimKerak.aloqa)
async def get_idora(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("🌐 Hudud:")
    await state.set_state(XodimKerak.hudud)

@router.message(XodimKerak.hudud)
async def get_idora(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("✍️Mas'ul ism sharifi?")
    await state.set_state(XodimKerak.masul)

@router.message(XodimKerak.masul)
async def get_idora(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("🕰 Murojaat qilish uchun qulay vaqt:")
    await state.set_state(XodimKerak.murojaat)

@router.message(XodimKerak.murojaat)
async def get_idora(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("🕒 Ish vaqti:")
    await state.set_state(XodimKerak.ish_vaqti)

@router.message(XodimKerak.ish_vaqti)
async def get_idora(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("💰 Maoshni kiriting?")
    await state.set_state(XodimKerak.maosh)

@router.message(XodimKerak.maosh)
async def get_idora(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("📝 Qushimcha ma'lumotlar:")
    await state.set_state(XodimKerak.qushimcha)
    data = await state.get_data()

    user_id = message.from_user.id
    username = f"@{message.from_user.username}" if message.from_user.username else "Noma’lum"

    text = (
        "📋 <b>Xodim kerak:</b>\n\n"
        f"🎓 Idora: {data['name']}\n"
        f"📚 Texnologiya: {data['texnologiya']}\n"
        f"🇺🇿 Telegram: {message.from_user.username}\n"
        f"📞 Aloqa: {data['aloqa']}\n"
        f"🌐 Hudud: {data['hudud']}\n"
        f"✍️Mas'ul ism sharifi: {data['masul']}\n"
        f"🕰 Murojaat qilish uchun qulay vaqt: {data['murojaat']}\n"
        f"🕒 Ish vaqti: {data['ish_vaqti']}\n"
        f"💰 Maosh: {data['maosh']}\n"
        f"📝 Qushimcha ma'lumotlar: {data['qushimcha']}\n\n"
        "#xodim"
    )

    admin_buttons = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ Tasdiqlash", callback_data=f"tasdiqla_{user_id}"),
                InlineKeyboardButton(text="❌ Rad etish", callback_data=f"rad_{user_id}"),
            ]
        ]
    )

    await message.bot.send_message(chat_id=ADMIN_ID, text=text, parse_mode="HTML", reply_markup=admin_buttons)

    await message.answer("✅ Ma’lumot adminga yuborildi. Tasdiqlash kutilmoqda.")
    await state.clear()


@router.callback_query(F.data.startswith("tasdiqla_"))
async def admin_confirm(call: CallbackQuery):
    user_id = int(call.data.split("_")[1])
    await call.message.edit_reply_markup()
    await call.message.answer("✅ Siz ushbu foydalanuvchini tasdiqladingiz.")
    await call.bot.send_message(user_id, "🎉 Sizning ma’lumotingiz admin tomonidan ✅ TASDIQLANDI!")

@router.callback_query(F.data.startswith("rad_"))
async def admin_reject(call: CallbackQuery):
    user_id = int(call.data.split("_")[1])
    await call.message.edit_reply_markup()
    await call.message.answer("❌ Siz ushbu foydalanuvchini rad etdingiz.")
    await call.bot.send_message(user_id, "😔 Sizning ma’lumotingiz admin tomonidan ❌ RAD ETILDI.")