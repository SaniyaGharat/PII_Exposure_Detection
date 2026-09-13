"""
PII Exposure Detection - OCR Engine Module
Provides optical character recognition extraction for scanned/degraded document images
using Tesseract (pytesseract) with seamless fallback to EasyOCR.
"""

import os
import shutil
from pathlib import Path
from typing import Optional, Union
from PIL import Image


class OCREngine:
    """Wrapper supporting Tesseract OCR with automatic fallback to EasyOCR."""

    def __init__(self, tesseract_cmd: Optional[str] = None):
        self.tesseract_cmd = tesseract_cmd or self._find_tesseract_binary()
        self.use_tesseract = False
        self.use_easyocr = False
        self.easyocr_reader = None

        # Try initializing Tesseract
        if self.tesseract_cmd:
            try:
                import pytesseract
                pytesseract.pytesseract.tesseract_cmd = self.tesseract_cmd
                self.use_tesseract = True
            except Exception:
                self.use_tesseract = False

        # If Tesseract not available, prepare EasyOCR fallback
        if not self.use_tesseract:
            try:
                import easyocr
                # Initialize EasyOCR reader for English (CPU mode for reliability)
                self.easyocr_reader = easyocr.Reader(["en"], gpu=False, verbose=False)
                self.use_easyocr = True
            except Exception:
                self.use_easyocr = False

    def _find_tesseract_binary(self) -> Optional[str]:
        """Locates tesseract executable on system PATH or standard Windows installation locations."""
        # 1. Check PATH
        path_which = shutil.which("tesseract")
        if path_which:
            return path_which

        # 2. Common Windows paths
        win_candidates = [
            r"C:\Program Files\Tesseract-OCR\tesseract.exe",
            r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
            os.path.expanduser(r"~\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"),
            os.path.expanduser(r"~\AppData\Local\Tesseract-OCR\tesseract.exe"),
        ]
        for candidate in win_candidates:
            if os.path.isfile(candidate):
                return candidate
        return None

    def extract_text(self, image_path: Union[str, Path]) -> str:
        """
        Extracts raw text from an image file.

        Args:
            image_path: Path to the scanned image (.png / .jpg).

        Returns:
            Extracted text string.
        """
        img_path = Path(image_path)
        if not img_path.exists():
            raise FileNotFoundError(f"Image not found at: {img_path}")

        image = Image.open(img_path)

        # 1. Tesseract
        if self.use_tesseract:
            try:
                import pytesseract
                text = pytesseract.image_to_string(image)
                if text and text.strip():
                    return text.strip()
            except Exception:
                pass  # Fall through to EasyOCR

        # 2. EasyOCR
        if self.easyocr_reader or self.use_easyocr:
            try:
                if self.easyocr_reader is None:
                    import easyocr
                    self.easyocr_reader = easyocr.Reader(["en"], gpu=False, verbose=False)
                results = self.easyocr_reader.readtext(str(img_path), detail=0, paragraph=True)
                return "\n".join(results).strip()
            except Exception:
                pass

        # 3. Basic fallback (if no OCR backend is active)
        return ""


# Module-level helper instance
_default_ocr_engine: Optional[OCREngine] = None


def extract_text_from_image(image_path: Union[str, Path]) -> str:
    """Convenience function to extract text using the default OCREngine instance."""
    global _default_ocr_engine
    if _default_ocr_engine is None:
        _default_ocr_engine = OCREngine()
    return _default_ocr_engine.extract_text(image_path)
