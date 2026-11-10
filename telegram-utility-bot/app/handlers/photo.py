from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

router = Router(name="photo_router")

@router.message(F.photo)
async def handle_photo(message: Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✂️ Xóa phông nền (Tách nền)", callback_data="action:rembg"),
        ],
        [
            InlineKeyboardButton(text="✨ Làm nét & Nâng cấp ảnh (2x)", callback_data="action:enhance"),
        ],
        [
            InlineKeyboardButton(text="📝 Bốc chữ từ ảnh (OCR)", callback_data="action:ocr"),
        ],
        [
            InlineKeyboardButton(text="🔄 Đổi sang PNG", callback_data="action:to_png"),
            InlineKeyboardButton(text="🔄 Đổi sang JPG", callback_data="action:to_jpg")
        ]
    ])
    
    await message.reply(
        "🖼️ <b>Đã nhận diện: Hình ảnh</b>\n"
        "Vui lòng chọn công cụ xử lý bạn muốn sử dụng:",
        reply_markup=keyboard,
        parse_mode="HTML"
    )
