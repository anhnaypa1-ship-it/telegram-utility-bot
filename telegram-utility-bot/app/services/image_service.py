import logging
from pathlib import Path
from PIL import Image, ImageEnhance, ImageOps

# Đăng ký plugin mở file HEIC của iPhone nếu có thư viện
try:
    import pillow_heif
    pillow_heif.register_heif_opener()
except ImportError:
    pass

logger = logging.getLogger(__name__)

def remove_background(input_path: Path, output_path: Path) -> None:
    """
    Xóa phông nền tự động bằng thư viện rembg với mô hình 'u2netp' (siêu nhẹ, tối ưu RAM).
    Kết quả trả về file PNG có nền trong suốt.
    """
    from rembg import remove, new_session
    
    # Dùng session với model u2netp để tiết kiệm bộ nhớ RAM (phù hợp với gói 512MB của Render)
    session = new_session("u2netp")
    
    with open(input_path, "rb") as f_in:
        input_data = f_in.read()
    
    output_data = remove(input_data, session=session)
    
    with open(output_path, "wb") as f_out:
        f_out.write(output_data)

def enhance_image(input_path: Path, output_path: Path) -> None:
    """
    Nâng cấp chất lượng ảnh: Làm nét (Sharpness), tăng độ tương phản (Contrast),
    cân bằng màu tự động và phóng to 2x (Upscale Lanczos).
    """
    with Image.open(input_path) as img:
        # Đảm bảo đúng chiều ảnh theo Exif
        img = ImageOps.exif_transpose(img)
        
        # Nếu là ảnh RGBA chuyển sang RGB khi lưu JPG
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
            
        # 1. Tự động cân bằng sáng & tương phản
        enhanced = ImageOps.autocontrast(img, cutoff=1)
        
        # 2. Tăng độ nét (Sharpness x1.6)
        sharpness_enhancer = ImageEnhance.Sharpness(enhanced)
        enhanced = sharpness_enhancer.enhance(1.6)
        
        # 3. Tăng độ tương phản nhẹ (Contrast x1.15)
        contrast_enhancer = ImageEnhance.Contrast(enhanced)
        enhanced = contrast_enhancer.enhance(1.15)
        
        # 4. Phóng to 2x (Upscale với bộ lọc Lanczos cao cấp)
        w, h = enhanced.size
        enhanced = enhanced.resize((w * 2, h * 2), Image.Resampling.LANCZOS)
        
        enhanced.save(output_path, format="JPEG", quality=95, optimize=True)

def convert_image(input_path: Path, output_path: Path, target_format: str = "PNG") -> None:
    """
    Chuyển đổi bất kỳ định dạng ảnh nào (kể cả HEIC của iPhone hay WebP) sang PNG hoặc JPG.
    """
    with Image.open(input_path) as img:
        img = ImageOps.exif_transpose(img)
        
        target_fmt = target_format.upper()
        if target_fmt in ("JPG", "JPEG"):
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")
            img.save(output_path, format="JPEG", quality=92, optimize=True)
        else:
            img.save(output_path, format="PNG", optimize=True)
