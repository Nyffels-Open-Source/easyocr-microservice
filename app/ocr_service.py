from typing import List
from pathlib import Path
from langdetect import detect
from concurrent.futures import ThreadPoolExecutor
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

def get_available_cpu_count() -> int:
    try:
        return len(os.sched_getaffinity(0))
    except AttributeError:
        return os.cpu_count() or 1

def extract_document_text(image_paths: List[Path]) -> OCRDocumentResult:
    initial_reader = easyocr.Reader(['en'], gpu=False)
    
    def run_ocr_initial(path: Path):
        return initial_reader.readtext(str(path))

    # Parallel OCR with 'en' to detect language
    with ThreadPoolExecutor(max_workers=get_available_cpu_count()) as executor:
        initial_results = list(executor.map(run_ocr_initial, image_paths))

    # Flatten results & get text for lang detection
    all_text = [item[1] for result in initial_results for item in result]
    combined_text = ' '.join(all_text)
    language = detect_language(combined_text)

    final_reader = easyocr.Reader([language], gpu=False)

    def run_ocr_final(path: Path):
        return final_reader.readtext(str(path))

    with ThreadPoolExecutor(max_workers=get_available_cpu_count()) as executor:
        final_results = list(executor.map(run_ocr_final, image_paths))

    final_text = [item[1] for result in final_results for item in result]
    confidences = [item[2] for result in final_results for item in result]

    confidence = round(sum(confidences) / len(confidences), 3) if confidences else 0.0

    return OCRDocumentResult(text=final_text, confidence=confidence, language=language)
