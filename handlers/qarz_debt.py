from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
import json
import os

router = Router()

class ViewByPhone(StatesGroup):
    phone = State()
    amount = State()  

def load_data(filename):
    if not os.path.exists(filename):
        return {"qarzlar": []} if filename=="qarzlar.json" else {"payloan": []}
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data, filename):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

@router.message(F.text == "Qarzni o'chirish(To'lash)")
async def qarzni_ochirish(message: Message, state: FSMContext):
    await message.answer("📞 Telefon raqamini kiriting:")
    await state.set_state(ViewByPhone.phone)

@router.message(ViewByPhone.phone)
async def get_phone(message: Message, state: FSMContext):
    phone_input = "".join(filter(str.isdigit, message.text)) 
    data = load_data("qarzlar.json")
    qarzlar = data.get("qarzlar", [])

    for qarz in qarzlar:
        qarz_phone = "".join(filter(str.isdigit, qarz.get("phone", "")))
        if qarz_phone == phone_input and qarz.get("is_active", True):
            await state.update_data(current_qarz_id=qarz.get("id"))
            await message.answer(
                f"💰 {qarz['full_name']} ni qarzi: {qarz['amount']:,} so‘m.\n"
                f"Qancha summa qaytarasiz?"
            )
            await state.set_state(ViewByPhone.amount)
            return

    await message.answer("⚠️ Bunday telefon raqamli faol qarz topilmadi.")
    await state.clear()

@router.message(ViewByPhone.amount)
async def get_amount(message: Message, state: FSMContext):
    try:
        pay_amount = int(message.text)
    except ValueError:
        await message.answer("⚠️ Iltimos, faqat raqam kiriting.")
        return

    state_data = await state.get_data()
    qarz_id = state_data.get("current_qarz_id")

    data = load_data("qarzlar.json")
    qarzlar = data.get("qarzlar", [])
    for qarz in qarzlar:
        if qarz.get("id") == qarz_id:
            original_amount = qarz["amount"]

            payloan_data = load_data("payloan.json")
            payloan_data.setdefault("payloan", [])

            if pay_amount >= original_amount:
                qarz["amount"] = 0
                qarz["is_active"] = False
                payloan_data["payloan"].append({**qarz, "paid_amount": original_amount})
                await message.answer(f"✅ {qarz['full_name']} qarzi to‘liq to‘landi ({original_amount:,} so‘m).")
            else:
                qarz["amount"] -= pay_amount
                payloan_data["payloan"].append({**qarz, "paid_amount": pay_amount})
                await message.answer(
                    f"✅ {qarz['full_name']} qarzidan {pay_amount:,} so‘m to‘landi.\n"
                    f"Qolgan qarz: {qarz['amount']:,} so‘m"
                )

            save_data(data, "qarzlar.json")
            save_data(payloan_data, "payloan.json")

            await state.clear()
            return
