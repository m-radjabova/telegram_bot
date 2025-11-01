from aiogram import Router, types, F
from services.pexels_api import search_pexels_images

router = Router()

@router.message(F.text)
async def search_images(message: types.Message):
    query = message.text.strip()

    if query.startswith('/'):
        return

    if len(query) < 2:
        await message.answer("❌ Iltimos, kamida 2 ta belgidan iborat so'z kiriting")
        return

    if len(query) > 50:
        await message.answer("❌ So'z juda uzun. Iltimos, qisqaroq so'z kiriting")
        return

    await message.answer(f"🔍 Qidirilmoqda: <b>{query}</b>")
    await search_pexels_images(message, query)
