import os
import zipfile
from pathlib import Path
from typing import Tuple, List
from pypdf import PdfReader, PdfWriter
from pdf2docx import Converter

def compress_pdf(input_path: Path, output_path: Path) -> Tuple[int, int]:
    """
    Nén file PDF bằng cách tối ưu luồng nội dung và giảm dung lượng metadata.
    Trả về: (dung lượng ban đầu, dung lượng sau nén tính theo bytes)
    """
    reader = PdfReader(str(input_path))
    writer = PdfWriter()

    for page in reader.pages:
        page.compress_content_streams()  # Nén các luồng nội dung
        writer.add_page(page)

    # Loại bỏ metadata thừa để giảm kích thước
    writer.add_metadata({})

    with open(output_path, "wb") as f:
        writer.write(f)

    orig_size = os.path.getsize(input_path)
    new_size = os.path.getsize(output_path)
    return orig_size, new_size

def pdf_to_word(input_path: Path, output_path: Path) -> None:
    """
    Chuyển đổi file PDF sang Word (.docx) giữ nguyên cấu trúc layout, bảng biểu và ảnh.
    """
    cv = Converter(str(input_path))
    try:
        cv.convert(str(output_path), start=0, end=None)
    finally:
        cv.close()

def extract_images_from_pdf(input_path: Path, output_dir: Path) -> List[Path]:
    """
    Trích xuất toàn bộ ảnh nhúng trong các trang của file PDF.
    """
    reader = PdfReader(str(input_path))
    extracted_images: List[Path] = []
    output_dir.mkdir(parents=True, exist_ok=True)

    img_counter = 1
    for page_idx, page in enumerate(reader.pages):
        for img_file in page.images:
            ext = Path(img_file.name).suffix or ".png"
            target_path = output_dir / f"image_p{page_idx + 1}_{img_counter}{ext}"
            with open(target_path, "wb") as f:
                f.write(img_file.data)
            extracted_images.append(target_path)
            img_counter += 1

    return extracted_images
