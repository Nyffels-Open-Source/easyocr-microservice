from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from pathlib import Path
import uuid
from zipfile import ZipFile
import shutil

from app.ocr_service import extract_document_text
from app.schema import OCRDocumentResult

UPLOAD_DIR = Path("/tmp/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

app = FastAPI(
    title="OCR Microservice",
    description="Extracts text from one or more uploaded images and detects the document's language.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post(
    "/ocr",
    response_model=OCRDocumentResult,
    summary="Perform OCR on uploaded images",
    description="Accepts multiple images that represent pages of a document. Performs OCR and returns the extracted text and detected language for the entire document."
)
async def ocr_images(files: List[UploadFile] = File(...)):
    image_paths = []

    try:
        for file in files:
            ext = Path(file.filename).suffix
            unique_name = f"{uuid.uuid4().hex}{ext}"
            path = UPLOAD_DIR / unique_name
            with open(path, "wb") as f:
                f.write(await file.read())
            image_paths.append(path)

        result = extract_document_text(image_paths)
        return result

    finally:
        for path in image_paths:
            path.unlink(missing_ok=True)

@app.post(
    "/ocr-zip",
    response_model=OCRDocumentResult,
    summary="Perform OCR on a zip file of images",
    description="Accepts a ZIP archive containing image files. Extracts and processes all supported images inside the archive."
)
async def ocr_zip(file: UploadFile = File(...)):
    if not file.filename.endswith(".zip"):
        return {"error": "Only .zip files are supported."}

    temp_dir = UPLOAD_DIR / uuid.uuid4().hex
    temp_dir.mkdir(parents=True, exist_ok=True)
    zip_path = temp_dir / "upload.zip"

    try:
        # Opslaan van de zip
        with open(zip_path, "wb") as f:
            f.write(await file.read())

        # Extractie
        with ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(temp_dir)

        # Filter enkel afbeelding bestanden
        image_paths = [p for p in temp_dir.rglob("*") if p.suffix.lower() in [".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".webp"]]

        if not image_paths:
            return {"error": "No supported image files found in the ZIP."}

        result = extract_document_text(image_paths)
        return result

    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)

@app.get(
    "/health",
    summary="Health check",
    description="Returns OK if the OCR service is running."
)
def health():
    return {"status": "ok"}
