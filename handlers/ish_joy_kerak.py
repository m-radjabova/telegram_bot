from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.fsm.context import FSMContext


from states.ish_joy_state import IshJoyKerak

ADMIN_ID = 7022476161
router = Router()

@router.message(F.text == "🏢 Ish joy kerak")
async def ish_joy_kerak(message: Message, state: FSMContext):
    await message.answer("✍️ Iltimos, to‘liq ismingizni kiriting:", reply_markup=ReplyKeyboardRemove())
    await state.set_state(IshJoyKerak.name)

@router.message(IshJoyKerak.name)
async def get_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("🕒 Yoshingizni kiriting:")
    await state.set_state(IshJoyKerak.age)

@router.message(IshJoyKerak.age)
async def get_age(message: Message, state: FSMContext):
    await state.update_data(age=message.text)
    await message.answer("📚 Qaysi texnologiyalarni bilasiz?")
    await state.set_state(IshJoyKerak.texnologiya)


@router.message(IshJoyKerak.texnologiya)
async def get_telegram(message: Message, state: FSMContext):
    await state.update_data(texnologiya=message.text)
    await message.answer("📞 Aloqa raqamingizni kiriting:")
    await state.set_state(IshJoyKerak.aloqa)

@router.message(IshJoyKerak.aloqa)
async def get_phone(message: Message, state: FSMContext):
    await state.update_data(aloqa=message.text)
    await message.answer("🌐 Qaysi hududdansiz?")
    await state.set_state(IshJoyKerak.hudud)

@router.message(IshJoyKerak.hudud)
async def get_hudud(message: Message, state: FSMContext):
    await state.update_data(hudud=message.text)
    await message.answer("💰 Sizning oylik kutgan narxingiz (so‘mda):")
    await state.set_state(IshJoyKerak.narxi)

@router.message(IshJoyKerak.narxi)
async def get_narxi(message: Message, state: FSMContext):
    await state.update_data(narxi=message.text)
    await message.answer("👨🏻‍💻 Kasbingizni kiriting:")
    await state.set_state(IshJoyKerak.kasbi)

@router.message(IshJoyKerak.kasbi)
async def get_kasbi(message: Message, state: FSMContext):
    await state.update_data(kasbi=message.text)
    await message.answer("🕰 Murojaat qilish uchun qulay vaqt:")
    await state.set_state(IshJoyKerak.murojaat)

@router.message(IshJoyKerak.murojaat)
async def get_murojaat(message: Message, state: FSMContext):
    await state.update_data(murojaat=message.text)
    await message.answer("🔎 Ish topishdan maqsadingiz nima?")
    await state.set_state(IshJoyKerak.maqsad)

@router.message(IshJoyKerak.maqsad)
async def get_maqsad(message: Message, state: FSMContext):
    await state.update_data(maqsad=message.text)
    data = await state.get_data()

    user_id = message.from_user.id
    username = f"@{message.from_user.username}" if message.from_user.username else "Noma’lum"

    text = (
        "📋 <b>Ish joyi kerak:</b>\n\n"
        f"👨‍💼 Xodim: {data['name']}\n"
        f"🕑 Yosh: {data['age']}\n"
        f"📚 Texnologiya: {data['texnologiya']}\n"
        f"🇺🇿 Telegram: {username}\n"
        f"📞 Aloqa: {data['aloqa']}\n"
        f"🌐 Hudud: {data['hudud']}\n"
        f"💰 Narxi: {data['narxi']}\n"
        f"👨🏻‍💻 Kasbi: {data['kasbi']}\n"
        f"🕰 Murojaat qilish vaqti: {data['murojaat']}\n"
        f"🔎 Maqsad: {data['maqsad']}\n\n"
        f"👤 <b>Foydalanuvchi ID:</b> <code>{user_id}</code>\n"
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