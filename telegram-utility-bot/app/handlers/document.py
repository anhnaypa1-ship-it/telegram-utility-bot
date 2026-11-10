from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

router = Router(name="document_router")

@router.message(F.document)
async def handle_document(message: Message):
    doc = message.document
    file_name = (doc.file_name or "file").lower()

    # 1. Nhóm tài liệu PDF
    if file_name.endswith(".pdf"):
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📉 Nén dung lượng PDF", callback_data="action:pdf_compress")],
            [InlineKeyboardButton(text="📄 Chuyển PDF sang Word (.docx)", callback_data="action:pdf_to_word")],
            [InlineKeyboardButton(text="🖼️ Trích xuất toàn bộ ảnh", callback_data="action:pdf_extract_img")],
        ])
        await message.reply(
            f"📄 <b>Đã nhận diện: Tài liệu PDF</b> (<code>{doc.file_name}</code>)\n"
            "Chọn chức năng xử lý:",
            reply_markup=keyboard,
            parse_mode="HTML"
        )
        return

    # 2. Nhóm ảnh gửi dưới dạng Document (HEIC iPhone, WebP, PNG, JPG)
    if file_name.endswith((".heic", ".webp", ".png", ".jpg", ".jpeg")):
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="✂️ Xóa phông nền", callback_data="action:rembg")],
            [InlineKeyboardButton(text="✨ Làm nét & Nâng cấp (2x)", callback_data="action:enhance")],
            [InlineKeyboardButton(text="📝 Bốc chữ từ ảnh (OCR)", callback_data="action:ocr")],
            [
                InlineKeyboardButton(text="🔄 Đổi sang JPG", callback_data="action:to_jpg"),
                InlineKeyboardButton(text="🔄 Đổi sang PNG", callback_data="action:to_png")
            ]
        ])
        await message.reply(
            f"🖼️ <b>Đã nhận diện: File ảnh gốc</b> (<code>{doc.file_name}</code>)\n"
            "Chọn thao tác xử lý:",
            reply_markup=keyboard,
            parse_mode="HTML"
        )
        return

    # 3. File nén
    if file_name.endswith((".zip", ".rar", ".7z")):
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📦 Xem danh sách & Giải nén", callback_data="action:archive_extract")]
        ])
        await message.reply(
            f"📦 <b>Đã nhận diện: File nén</b> (<code>{doc.file_name}</code>):",
            reply_markup=keyboard,
            parse_mode="HTML"
        )
        return

    await message.reply(
        f"📁 Đã nhận file <code>{doc.file_name}</code>.\n"
        "Hiện bot đang ưu tiên hỗ trợ xử lý <b>PDF</b>, <b>Ảnh (Xóa nền, Làm nét, OCR)</b> và <b>File nén</b>.",
        parse_mode="HTML"
    )
