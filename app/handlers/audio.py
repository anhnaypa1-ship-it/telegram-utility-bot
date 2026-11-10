from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

router = Router(name="audio_router")

@router.message(F.audio | F.voice | F.video)
async def handle_media(message: Message):
    if message.audio:
        media_type = "File âm thanh"
    elif message.voice:
        media_type = "Tin nhắn thoại"
    else:
        media_type = "Video"

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎵 Trích xuất thành file MP3", callback_data="action:to_mp3")],
        [InlineKeyboardButton(text="🎙️ Gõ thành văn bản (Speech-to-Text)", callback_data="action:transcribe")],
    ])

    await message.reply(
        f"🎙️ **Đã nhận diện: {media_type}**\n"
        "Chọn tính năng bạn muốn sử dụng:",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )
