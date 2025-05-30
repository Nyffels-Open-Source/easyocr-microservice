from pydantic import BaseModel
from typing import List

class OCRDocumentResult(BaseModel):
    text: List[str]
    confidence: float
    language: str
