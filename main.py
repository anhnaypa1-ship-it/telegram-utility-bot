import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from app.config import BOT_TOKEN, PORT
from app.web import start_web_server
from app.handlers import register_all_handlers

# Thiết lập log ra màn hình console
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("main")

async def main():
    if not BOT_TOKEN:
        logger.error(
            "\n❌ LỖI: Chưa cấu hình BOT_TOKEN!\n"
            "👉 Hãy mở file 'D:\\telegram-utility-bot\\.env' và dán API Token nhận được từ @BotFather vào."
        )
        return

    logger.info("🚀 Đang khởi động hệ thống Telegram Utility Bot...")

    # 1. Khởi tạo Bot và Dispatcher của aiogram 3
    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()

    # 2. Đăng ký toàn bộ Router xử lý sự kiện
    register_all_handlers(dp)

    # 3. Khởi động Web Server (Health Check cho Render / Cron-job)
    web_runner = await start_web_server(PORT)

    # 4. Bắt đầu lắng nghe tin nhắn từ Telegram (Long Polling)
    try:
        logger.info("🤖 Bot Telegram đã sẵn sàng nhận tin nhắn!")
        # Xóa các update bị nghẽn trước đó khi bot offline
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        logger.info("🛑 Đang đóng các kết nối...")
        await bot.session.close()
        await web_runner.cleanup()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("👋 Bot đã dừng an toàn.")
