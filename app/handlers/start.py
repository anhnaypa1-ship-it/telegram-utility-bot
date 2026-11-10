from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

router = Router(name="start_router")

@router.message(CommandStart())
async def cmd_start(message: Message):
    user_name = message.from_user.first_name if message.from_user else "bạn"
    text = (
        f"👋 Xin chào **{user_name}**!\n\n"
        "Chào mừng bạn đến với **Bot Tiện Ích Đa Năng (All-in-One Utility)**.\n"
        "Chỉ cần gửi file vào đây, bot sẽ tự nhận diện định dạng và hỗ trợ bạn xử lý:\n\n"
        "🖼️ **Gửi ảnh:** Xóa phông nền, Bốc chữ OCR, Đổi đuôi ảnh.\n"
        "📄 **Gửi tài liệu (PDF, Word):** Nén dung lượng, Đổi Word <-> PDF.\n"
        "🎵 **Gửi âm thanh / video:** Trích xuất MP3, Gõ văn bản từ giọng nói.\n"
        "📦 **Gửi file nén (.zip, .rar):** Xem danh sách và giải nén ngay.\n\n"
        "💡 *Hãy thử gửi một tấm ảnh hoặc một file tài liệu bất kỳ để bắt đầu!*"
    )
    await message.answer(text, parse_mode="Markdown")

@router.message(Command("help"))
async def cmd_help(message: Message):
    text = (
        "📖 **HƯỚNG DẪN SỬ DỤNG:**\n\n"
        "1. **Ảnh:** Gửi ảnh trực tiếp (hoặc gửi dưới dạng file .png, .jpg, .webp, .heic).\n"
        "2. **Tài liệu:** Gửi file .pdf hoặc .docx để nén hoặc chuyển đổi định dạng.\n"
        "3. **Âm thanh:** Gửi file mp3, m4a, wav hoặc tin nhắn thoại.\n"
        "4. **File nén:** Gửi file .zip để bung file trực tiếp.\n\n"
        "Mọi thắc mắc hoặc góp ý tính năng, hãy liên hệ admin!"
    )
    await message.answer(text, parse_mode="Markdown")
