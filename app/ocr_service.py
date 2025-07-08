from typing import List
from pathlib import Path
from langdetect import detect
import easyocr
import os

from app.schema import OCRDocumentResult

SUPPORTED_LANGUAGES = ['en', 'nl', 'fr', 'de']

def detect_language(text: str) -> str:
    try:
        lang = detect(text)
        return lang if lang in SUPPORTED_LANGUAGES else 'en'
    except Exception:
        return 'en'

def extract_document_text(image_paths: List[Path]) -> OCRDocumentResult:
    reader = easyocr.Reader(['en'], gpu=False, thread_count=get_available_cpu_count())
    all_text = []

    for path in image_paths:
        results = reader.readtext(str(path))
        all_text.extend([item[1] for item in results])

    combined_text = ' '.join(all_text)
    language = detect_language(combined_text)

    final_reader = easyocr.Reader([language], gpu=False, thread_count=get_available_cpu_count())
    final_text = []
    confidences = []

    for path in image_paths:
        results = final_reader.readtext(str(path))
        final_text.extend([item[1] for item in results])
        confidences.extend([item[2] for item in results])

    confidence = round(sum(confidences) / len(confidences), 3) if confidences else 0.0

    return OCRDocumentResult(text=final_text, confidence=confidence, language=language)

def get_available_cpu_count():
    try:
        return len(os.sched_getaffinity(0))
    except AttributeError:
        return os.cpu_count() or 1