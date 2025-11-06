import uuid
from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
import json
import os
from datetime import datetime

router = Router()

class QarzForm(StatesGroup):
    full_name = State()
    address = State()
    phone = State()
    amount = State()

def load_data():
    if not os.path.exists("qarzlar.json"):
        return {"qarzlar": []}
    with open("qarzlar.json", "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    with open("qarzlar.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

@router.message(F.text == "Qarz Berish")
async def start_qarz(message: Message, state: FSMContext):
    await message.answer("🧾 Qarz oluvchining to‘liq ismini kiriting:")
    await state.set_state(QarzForm.full_name)

@router.message(QarzForm.full_name)
async def get_name(message: Message, state: FSMContext):
    await state.update_data(full_name=message.text)
    await message.answer("🏠 Manzilini kiriting:")
    await state.set_state(QarzForm.address)

@router.message(QarzForm.address)
async def get_address(message: Message, state: FSMContext):
    await state.update_data(address=message.text)
    await message.answer("📞 Telefon raqamini kiriting:")
    await state.set_state(QarzForm.phone)

@router.message(QarzForm.phone)
async def get_phone(message: Message, state: FSMContext):
    await state.update_data(phone=message.text)
    await message.answer("💰 Qarz summasini kiriting (so‘mda):")
    await state.set_state(QarzForm.amount)

@router.message(QarzForm.amount)
async def get_amount(message: Message, state: FSMContext):
    try:
        amount = int(message.text)
    except ValueError:
        await message.answer("⚠️ Iltimos, faqat raqam kiriting.")
        return

    await state.update_data(amount=amount)

    data = await state.get_data()
    data["id"] = str(uuid.uuid4())
    data["date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data["is_active"] = True

    all_data = load_data()
    all_data["qarzlar"].append(data)
    save_data(all_data)

    await message.answer(
        f"✅ Siz <b>{data['full_name']}</b> ga <b>{data['amount']:,}</b> so‘m qarz berdingiz.\n\n"
        f"📅 Sana: {data['date']}\n"
        f"🏠 Manzil: {data['address']}\n"
        f"📞 Tel: {data['phone']}"
    )
    await state.clear()