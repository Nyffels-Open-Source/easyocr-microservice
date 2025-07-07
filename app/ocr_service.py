from typing import List
from pathlib import Path
from langdetect import detect
import easyocr

from app.schema import OCRDocumentResult

SUPPORTED_LANGUAGES = ['en', 'nl', 'fr', 'de']

def detect_language(text: str) -> str:
    try:
        lang = detect(text)
        return lang if lang in SUPPORTED_LANGUAGES else 'en'
    except Exception:
        return 'en'

def extract_document_text(image_paths: List[Path], psm: int = 6) -> OCRDocumentResult:
    reader = easyocr.Reader(['en'], gpu=False)
    all_text = []

    for path in image_paths:
        results = reader.readtext(str(path), detail=1, paragraph=False, config=f'--psm {psm}')
        all_text.extend([item[1] for item in results])

    combined_text = ' '.join(all_text)
    language = detect_language(combined_text)

    final_reader = easyocr.Reader([language], gpu=False)
    final_text = []
    confidences = []

    for path in image_paths:
        results = final_reader.readtext(str(path))
        final_text.extend([item[1] for item in results])
        confidences.extend([item[2] for item in results])

    confidence = round(sum(confidences) / len(confidences), 3) if confidences else 0.0

    return OCRDocumentResult(text=final_text, confidence=confidence, language=language)
