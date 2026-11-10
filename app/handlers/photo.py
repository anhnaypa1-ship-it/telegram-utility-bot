from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

router = Router(name="photo_router")

@router.message(F.photo)
async def handle_photo(message: Message):
    # Lấy ảnh có chất lượng cao nhất trong danh sách photo
    photo = message.photo[-1]
    file_id = photo.file_id
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✂️ Xóa phông nền (Tách nền)", callback_data=f"photo:rembg:{file_id}"),
        ],
        [
            InlineKeyboardButton(text="✨ Làm nét & Nâng cấp ảnh (2x)", callback_data=f"photo:enhance:{file_id}"),
        ],
        [
            InlineKeyboardButton(text="📝 Bốc chữ từ ảnh (OCR)", callback_data=f"photo:ocr:{file_id}"),
        ],
        [
            InlineKeyboardButton(text="🔄 Đổi sang PNG", callback_data=f"photo:to_png:{file_id}"),
            InlineKeyboardButton(text="🔄 Đổi sang JPG", callback_data=f"photo:to_jpg:{file_id}")
        ]
    ])
    
    await message.reply(
        "🖼️ **Đã nhận diện: Hình ảnh**\n"
        "Vui lòng chọn công cụ xử lý bạn muốn sử dụng:",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )
