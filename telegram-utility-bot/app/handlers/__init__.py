from aiogram import Dispatcher
from .start import router as start_router
from .photo import router as photo_router
from .document import router as document_router
from .audio import router as audio_router
from .callbacks import router as callback_router

def register_all_handlers(dp: Dispatcher):
    """Đăng ký tất cả các Router xử lý tin nhắn vào Dispatcher chính"""
    dp.include_router(start_router)
    dp.include_router(photo_router)
    dp.include_router(document_router)
    dp.include_router(audio_router)
    dp.include_router(callback_router)
