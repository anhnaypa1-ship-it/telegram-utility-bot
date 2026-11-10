# 🤖 Telegram Utility Bot (PDF Toolkit, OCR & AI Image Enhancer)

Bot Telegram tiện ích đa năng mã nguồn mở, tích hợp sẵn 3 nhóm tính năng thực chiến:
1. **📄 "All-in-One" PDF Toolkit:** Nén dung lượng PDF, chuyển PDF sang Word (`.docx`), trích xuất hình ảnh.
2. **📝 Bot OCR Bốc chữ:** Dùng AI (Google Gemini Vision) đọc chữ tiếng Việt, hóa đơn, bảng biểu và chữ viết tay từ ảnh.
3. **✂️ AI Image Tools:** Xóa phông nền (Rembg model u2netp nhẹ & mượt), Làm nét & Phóng to ảnh 2x, Xử lý ảnh iPhone (HEIC) và WebP.

---

## 📁 Cấu trúc thư mục dự án

```
D:\telegram-utility-bot\
├── app/
│   ├── handlers/            # Bộ lọc sự kiện tin nhắn
│   │   ├── photo.py         # Nhận diện ảnh -> Menu xóa nền, làm nét, OCR, đổi đuôi
│   │   ├── document.py      # Nhận diện PDF, ảnh gốc, file nén
│   │   ├── callbacks.py     # Điều phối tải file -> xử lý -> gửi kết quả -> dọn dẹp
│   │   ├── start.py         # Lệnh /start, /help
│   │   └── audio.py         # Xử lý âm thanh
│   ├── services/            # Các module xử lý lõi
│   │   ├── pdf_service.py   # Nén PDF, PDF -> Word (.docx), trích xuất ảnh
│   │   ├── ocr_service.py   # AI OCR bốc chữ tiếng Việt qua Gemini API
│   │   └── image_service.py # Xóa phông (Rembg), Làm nét & Phóng to 2x, Convert HEIC/PNG/JPG
│   ├── config.py            # Quản lý cấu hình & thư mục tạm
│   └── web.py               # Cổng web /health cho Render & cron-job.org
├── .env                     # Chứa BOT_TOKEN & GEMINI_API_KEY (Không đưa lên GitHub)
├── render.yaml              # Cấu hình 1-click deploy Render
├── requirements.txt         # Thư viện Python
├── main.py                  # File khởi động ứng dụng
└── README.md
```

---

## 🔑 Hướng dẫn cấu hình API Token & Key (Miễn phí 100%)

Mở file **[`.env`](file:///D:/telegram-utility-bot/.env)** và điền 2 giá trị sau:

1. **`BOT_TOKEN`**:
   - Mở Telegram tìm bot **`@BotFather`**.
   - Gõ `/newbot`, đặt tên và sao chép mã Token dán vào.

2. **`GEMINI_API_KEY`**:
   - Truy cập **[Google AI Studio](https://aistudio.google.com/app/apikey)**.
   - Đăng nhập tài khoản Google và bấm **Create API key** (Hoàn toàn miễn phí, hạn mức ~1.500 lượt đọc ảnh/ngày).
   - Sao chép API Key dán vào `.env`.

---

## 🚀 Triển khai lên Render & Giữ chạy 24/7

1. Đưa toàn bộ thư mục `D:\telegram-utility-bot` lên **GitHub**.
2. Trên **Render.com**:
   - Tạo **New Web Service** kết nối với repo GitHub.
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python main.py`
   - Trong phần **Environment Variables**, thêm:
     - `BOT_TOKEN`: Token của Telegram
     - `GEMINI_API_KEY`: Key của Google Gemini
3. Trên **cron-job.org**:
   - Tạo cronjob ping link `https://tên-dự-án.onrender.com/health` mỗi **10 phút/lần**.
   - Bot sẽ trực tuyến 24/7 mà không bao giờ bị Render đưa vào trạng thái ngủ!
