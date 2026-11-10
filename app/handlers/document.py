from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

router = Router(name="document_router")

@router.message(F.document)
async def handle_document(message: Message):
    doc = message.document
    file_name = (doc.file_name or "file").lower()
    file_id = doc.file_id

    # 1. Nhóm tài liệu PDF
    if file_name.endswith(".pdf"):
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📉 Nén dung lượng PDF", callback_data=f"doc:pdf_compress:{file_id}")],
            [InlineKeyboardButton(text="📄 Chuyển PDF sang Word (.docx)", callback_data=f"doc:pdf_to_word:{file_id}")],
            [InlineKeyboardButton(text="🖼️ Trích xuất toàn bộ ảnh", callback_data=f"doc:pdf_extract_img:{file_id}")],
        ])
        await message.reply(
            f"📄 **Đã nhận diện: Tài liệu PDF** (`{doc.file_name}`)\n"
            "Chọn chức năng xử lý:",
            reply_markup=keyboard,
            parse_mode="Markdown"
        )
        return

    # 2. Nhóm ảnh gửi dưới dạng Document (HEIC iPhone, WebP, PNG, JPG)
    if file_name.endswith((".heic", ".webp", ".png", ".jpg", ".jpeg")):
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="✂️ Xóa phông nền", callback_data=f"doc:rembg:{file_id}")],
            [InlineKeyboardButton(text="✨ Làm nét & Nâng cấp (2x)", callback_data=f"doc:enhance:{file_id}")],
            [InlineKeyboardButton(text="📝 Bốc chữ từ ảnh (OCR)", callback_data=f"doc:ocr:{file_id}")],
            [
                InlineKeyboardButton(text="🔄 Đổi sang JPG", callback_data=f"doc:to_jpg:{file_id}"),
                InlineKeyboardButton(text="🔄 Đổi sang PNG", callback_data=f"doc:to_png:{file_id}")
            ]
        ])
        await message.reply(
            f"🖼️ **Đã nhận diện: File ảnh gốc** (`{doc.file_name}`)\n"
            "Chọn thao tác xử lý:",
            reply_markup=keyboard,
            parse_mode="Markdown"
        )
        return

    # 3. File nén
    if file_name.endswith((".zip", ".rar", ".7z")):
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📦 Xem danh sách & Giải nén", callback_data=f"archive:extract:{file_id}")]
        ])
        await message.reply(
            f"📦 **Đã nhận diện: File nén** (`{doc.file_name}`):",
            reply_markup=keyboard,
            parse_mode="Markdown"
        )
        return

    await message.reply(
        f"📁 Đã nhận file `{doc.file_name}`.\n"
        "Hiện bot đang ưu tiên hỗ trợ xử lý **PDF**, **Ảnh (Xóa nền, Làm nét, OCR)** và **File nén**.",
        parse_mode="Markdown"
    )
