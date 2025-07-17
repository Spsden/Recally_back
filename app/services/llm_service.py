
from .llm_providers import llm_service

def transcribe_audio(file_path: str):
    return llm_service.transcribe_audio(file_path)

def summarize_text(text: str):
    return llm_service.summarize_text(text)

def ocr_image(file_path: str):
    return llm_service.ocr_image(file_path)
