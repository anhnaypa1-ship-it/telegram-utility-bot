import os
import shutil
import uuid
import asyncio
import logging
from pathlib import Path

from aiogram import Router, Bot
from aiogram.types import CallbackQuery, FSInputFile

from app.config import TEMP_DIR
from app.services.pdf_service import compress_pdf, pdf_to_word, extract_images_from_pdf
from app.services.ocr_service import extract_text_from_image
from app.services.image_service import remove_background, enhance_image, convert_image

logger = logging.getLogger(__name__)
router = Router(name="callback_router")

@router.callback_query()
async def process_all_callbacks(callback: CallbackQuery, bot: Bot):
    await callback.answer()  # Tắt hiệu ứng xoay tròn ở nút bấm Telegram
    data = callback.data or ""
    
    if not data.startswith("action:"):
        return

    action = data.split(":", 1)[1]
    
    # Lấy tin nhắn gốc chứa file mà bot vừa reply
    target_msg = callback.message.reply_to_message
    if not target_msg:
        await callback.message.reply("⚠️ Không tìm thấy file gốc! Hãy gửi lại file cho bot nhé.")
        return

    # Lấy file_id từ tin nhắn gốc
    file_id = None
    file_name = "file"
    
    if target_msg.photo:
        file_id = target_msg.photo[-1].file_id
        file_name = "image.jpg"
    elif target_msg.document:
        file_id = target_msg.document.file_id
        file_name = target_msg.document.file_name or "document"
    elif target_msg.audio:
        file_id = target_msg.audio.file_id
        file_name = target_msg.audio.file_name or "audio.mp3"
    elif target_msg.voice:
        file_id = target_msg.voice.file_id
        file_name = "voice.ogg"
    elif target_msg.video:
        file_id = target_msg.video.file_id
        file_name = "video.mp4"

    if not file_id:
        await callback.message.reply("⚠️ Không tìm thấy dữ liệu file trong tin nhắn này.")
        return

    # Tạo thư mục làm việc riêng cho từng task để tránh xung đột
    task_id = str(uuid.uuid4())[:8]
    work_dir = TEMP_DIR / task_id
    work_dir.mkdir(parents=True, exist_ok=True)
    
    status_msg = await callback.message.reply("⏳ Đang tải file về máy chủ...")

    try:
        # 1. Tải file từ Telegram về thư mục tạm
        file_info = await bot.get_file(file_id)
        original_ext = Path(file_info.file_path).suffix or Path(file_name).suffix or ".dat"
        input_file = work_dir / f"input_{task_id}{original_ext}"
        
        await bot.download(file_info, destination=input_file)
        await status_msg.edit_text("⚙️ Đang xử lý... Vui lòng đợi trong giây lát.")

        # ==================== NHÓM 1: XỬ LÝ ẢNH & OCR ====================
        
        # A. Xóa phông nền (Rembg)
        if action == "rembg":
            output_file = work_dir / f"transparent_{task_id}.png"
            await asyncio.to_thread(remove_background, input_file, output_file)
            
            await status_msg.edit_text("📤 Đang gửi ảnh đã xóa nền...")
            await callback.message.reply_document(
                document=FSInputFile(output_file, filename="background_removed.png"),
                caption="✅ Đã xóa phông nền thành công (Ảnh PNG trong suốt)."
            )

        # B. Làm nét & Nâng cấp ảnh (Enhance)
        elif action == "enhance":
            output_file = work_dir / f"enhanced_{task_id}.jpg"
            await asyncio.to_thread(enhance_image, input_file, output_file)
            
            await status_msg.edit_text("📤 Đang gửi ảnh đã nâng cấp...")
            await callback.message.reply_photo(
                photo=FSInputFile(output_file),
                caption="✨ Đã tăng độ nét, cân bằng màu và phóng to 2x thành công!"
            )

        # C. Bốc chữ OCR
        elif action == "ocr":
            await status_msg.edit_text("🔍 AI đang nhận diện chữ trong ảnh...")
            ocr_text = await extract_text_from_image(input_file)
            
            if len(ocr_text) > 3800:
                txt_file = work_dir / "extracted_text.txt"
                txt_file.write_text(ocr_text, encoding="utf-8")
                await callback.message.reply_document(
                    document=FSInputFile(txt_file, filename="noi_dung_ocr.txt"),
                    caption="📝 Văn bản quá dài, bot đã lưu vào file .txt cho bạn."
                )
            else:
                # Gửi văn bản thuần túy không dùng parse_mode để tránh lỗi ký tự đặc biệt
                await callback.message.reply(
                    f"📝 NỘI DUNG VĂN BẢN TRÍCH XUẤT ĐƯỢC:\n\n{ocr_text}"
                )

        # D. Đổi đuôi ảnh (Sang JPG hoặc PNG)
        elif action in ("to_png", "to_jpg"):
            target_fmt = "PNG" if action == "to_png" else "JPG"
            ext = ".png" if action == "to_png" else ".jpg"
            output_file = work_dir / f"converted_{task_id}{ext}"
            
            await asyncio.to_thread(convert_image, input_file, output_file, target_fmt)
            await callback.message.reply_document(
                document=FSInputFile(output_file, filename=f"image_{task_id}{ext}"),
                caption=f"✅ Đã chuyển đổi sang định dạng {target_fmt} thành công!"
            )

        # ==================== NHÓM 2: BỘ CÔNG CỤ PDF ====================

        # E. Nén dung lượng PDF
        elif action == "pdf_compress":
            output_file = work_dir / f"compressed_{task_id}.pdf"
            orig_size, new_size = await asyncio.to_thread(compress_pdf, input_file, output_file)
            
            orig_mb = orig_size / (1024 * 1024)
            new_mb = new_size / (1024 * 1024)
            saved_pct = max(0, int((orig_size - new_size) / orig_size * 100)) if orig_size > 0 else 0

            caption = (
                f"✅ <b>Đã nén file PDF thành công!</b>\n"
                f"📊 Dung lượng gốc: <code>{orig_mb:.2f} MB</code>\n"
                f"📉 Sau khi nén: <code>{new_mb:.2f} MB</code>\n"
                f"🎉 Tiết kiệm: <b>{saved_pct}%</b>"
            )
            await callback.message.reply_document(
                document=FSInputFile(output_file, filename="compressed_document.pdf"),
                caption=caption,
                parse_mode="HTML"
            )

        # F. Chuyển PDF sang Word (.docx)
        elif action == "pdf_to_word":
            output_file = work_dir / f"converted_{task_id}.docx"
            await asyncio.to_thread(pdf_to_word, input_file, output_file)
            
            await callback.message.reply_document(
                document=FSInputFile(output_file, filename="document_converted.docx"),
                caption="✅ Đã chuyển đổi PDF sang Word (.docx) giữ nguyên cấu trúc layout và bảng!"
            )

        # G. Trích xuất toàn bộ ảnh từ PDF
        elif action == "pdf_extract_img":
            img_dir = work_dir / "extracted_images"
            images = await asyncio.to_thread(extract_images_from_pdf, input_file, img_dir)
            
            if not images:
                await callback.message.reply("ℹ️ Không tìm thấy hình ảnh nào được nhúng bên trong file PDF này.")
            else:
                await status_msg.edit_text(f"📤 Đang gửi {len(images)} ảnh trích xuất được...")
                for img_path in images[:10]:
                    await callback.message.reply_photo(photo=FSInputFile(img_path))
                if len(images) > 10:
                    await callback.message.reply(f"ℹ️ Đã gửi 10 ảnh đầu tiên trong tổng số {len(images)} ảnh.")

        else:
            await callback.message.reply(f"⚠️ Tính năng <code>{action}</code> đang được tối ưu hóa.", parse_mode="HTML")

        # Xóa tin nhắn trạng thái chờ sau khi hoàn tất
        await status_msg.delete()

    except Exception as e:
        logger.error(f"Lỗi khi xử lý callback action={action}: {e}", exc_info=True)
        await status_msg.edit_text(f"❌ Đã xảy ra lỗi trong quá trình xử lý: {str(e)}")

    finally:
        # Tự động dọn dẹp thư mục tạm để bảo vệ dung lượng ổ cứng
        shutil.rmtree(work_dir, ignore_errors=True)
