from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

router = Router(name="audio_router")

@router.message(F.audio | F.voice | F.video)
async def handle_media(message: Message):
    if message.audio:
        media_type = "File âm thanh"
        file_id = message.audio.file_id
    elif message.voice:
        media_type = "Tin nhắn thoại"
        file_id = message.voice.file_id
    else:
        media_type = "Video"
        file_id = message.video.file_id

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎵 Trích xuất thành file MP3", callback_data=f"audio:to_mp3:{file_id}")],
        [InlineKeyboardButton(text="🎙️ Gõ thành văn bản (Speech-to-Text)", callback_data=f"audio:transcribe:{file_id}")],
    ])

    await message.reply(
        f"🎙️ **Đã nhận diện: {media_type}**\n"
        "Chọn tính năng bạn muốn sử dụng:",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )
