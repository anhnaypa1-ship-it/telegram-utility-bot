from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

router = Router(name="start_router")

@router.message(CommandStart())
async def cmd_start(message: Message):
    user_name = message.from_user.first_name if message.from_user else "bạn"
    text = (
        f"👋 Xin chào <b>{user_name}</b>!\n\n"
        "Chào mừng bạn đến với <b>Bot Tiện Ích Đa Năng (All-in-One Utility)</b>.\n"
        "Chỉ cần gửi file vào đây, bot sẽ tự nhận diện định dạng và hỗ trợ bạn xử lý:\n\n"
        "🖼️ <b>Gửi ảnh:</b> Xóa phông nền, Bốc chữ OCR, Đổi đuôi ảnh.\n"
        "📄 <b>Gửi tài liệu (PDF, Word):</b> Nén dung lượng, Đổi Word &lt;-&gt; PDF.\n"
        "🎵 <b>Gửi âm thanh / video:</b> Trích xuất MP3, Gõ văn bản từ giọng nói.\n"
        "📦 <b>Gửi file nén (.zip, .rar):</b> Xem danh sách và giải nén ngay.\n\n"
        "💡 <i>Hãy thử gửi một tấm ảnh hoặc một file tài liệu bất kỳ để bắt đầu!</i>"
    )
    await message.answer(text, parse_mode="HTML")

@router.message(Command("help"))
async def cmd_help(message: Message):
    text = (
        "📖 <b>HƯỚNG DẪN SỬ DỤNG:</b>\n\n"
        "1. <b>Ảnh:</b> Gửi ảnh trực tiếp (hoặc gửi dưới dạng file .png, .jpg, .webp, .heic).\n"
        "2. <b>Tài liệu:</b> Gửi file .pdf hoặc .docx để nén hoặc chuyển đổi định dạng.\n"
        "3. <b>Âm thanh:</b> Gửi file mp3, m4a, wav hoặc tin nhắn thoại.\n"
        "4. <b>File nén:</b> Gửi file .zip để bung file trực tiếp.\n\n"
        "Mọi thắc mắc hoặc góp ý tính năng, hãy liên hệ admin!"
    )
    await message.answer(text, parse_mode="HTML")
