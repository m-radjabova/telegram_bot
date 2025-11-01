from aiogram import Router, types, F
from services.pexels_api import search_pexels_images

router = Router()

@router.callback_query(F.data.startswith("search_"))
async def handle_search_categories(callback: types.CallbackQuery):
    search_map = {
        "search_nature": "beautiful nature",
        "search_animals": "cute animals",
        "search_cars": "luxury cars",
        "search_food": "delicious food"
    }
    query = search_map[callback.data]
    await callback.message.delete()
    await search_pexels_images(callback.message, query)
    await callback.answer()

@router.callback_query(F.data.startswith("new_"))
async def handle_new_image(callback: types.CallbackQuery):
    query = callback.data.replace("new_", "")
    await callback.message.delete()
    await search_pexels_images(callback.message, query)
    await callback.answer("🔄 Yangi rasm yuklanmoqda...")

@router.callback_query(F.data.startswith("like_"))
async def handle_like(callback: types.CallbackQuery):
    await callback.answer("❤️ Sizga rasm yoqdi!", show_alert=False)
