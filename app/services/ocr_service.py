import logging
from pathlib import Path
from PIL import Image
from app.config import GEMINI_API_KEY

logger = logging.getLogger(__name__)

async def extract_text_from_image(image_path: Path) -> str:
    """
    Sử dụng Google Gemini Vision API để nhận diện chữ tiếng Việt,
    bảng biểu, hóa đơn và chữ viết tay từ hình ảnh.
    """
    if not GEMINI_API_KEY:
        return (
            "⚠️ **Chưa cấu hình GEMINI_API_KEY!**\n\n"
            "Để kích hoạt tính năng Bốc chữ OCR miễn phí:\n"
            "1. Truy cập https://aistudio.google.com/app/apikey tạo key miễn phí.\n"
            "2. Thêm `GEMINI_API_KEY=your_key` vào file `.env` hoặc phần Environment Variables trên Render."
        )

    try:
        from google import genai
        client = genai.Client(api_key=GEMINI_API_KEY)

        # Mở ảnh bằng Pillow
        img = Image.open(image_path)

        prompt = (
            "Bạn là chuyên gia OCR văn bản. Hãy đọc và trích xuất toàn bộ nội dung chữ trong ảnh này.\n"
            "- Nhận diện chính xác tiếng Việt, cả chữ in và chữ viết tay.\n"
            "- Giữ nguyên định dạng xuống dòng, danh sách gạch đầu dòng hoặc bảng biểu (nếu có định dạng markdown table).\n"
            "- Chỉ trả về nội dung văn bản trích xuất được, tuyệt đối không thêm lời chào hoặc bình luận thừa."
        )

        # Thử với model gemini-2.5-flash hoặc gemini-2.0-flash / 1.5-flash
        model_name = "gemini-2.5-flash"
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=[img, prompt]
            )
        except Exception:
            # Fallback sang gemini-2.0-flash hoặc gemini-1.5-flash
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=[img, prompt]
            )

        result_text = response.text or ""
        if not result_text.strip():
            return "🔍 Không phát hiện thấy nội dung chữ nào rõ ràng trong bức ảnh này."

        return result_text.strip()

    except Exception as e:
        logger.error(f"Lỗi khi gọi Gemini OCR: {e}", exc_info=True)
        return f"❌ Lỗi xử lý OCR: {str(e)}"
