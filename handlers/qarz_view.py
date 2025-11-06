from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from handlers.qarz import load_data

router = Router()

@router.message(F.text == "Qarzlar ro'yxati")
async def show_all_qarzlar(message: Message, state: FSMContext):
    data = load_data()
    qarzlar = data.get("qarzlar", [])

    if not qarzlar:
        await message.answer("⚠️ Hozircha qarzlar ro‘yxati bo‘sh.")
        return

    text_lines = ["📋 Barcha qarzlar ro'yxati:\n"]
    for i, q in enumerate(qarzlar, 1):
        text_lines.append(
            f"👤 name: {q.get('full_name','—')}\n"
            f"💰 amount: {q.get('amount','0'):,} so'm\n"
            f"📅 time: {q.get('date','—')}\n"
            f"🏠 address: {q.get('address','—')}\n"
            f"📞 phone: {q.get('phone','—')}\n"
            f"-------------------------------\n"
        )

    await message.answer("\n".join(text_lines))
    await state.clear()
