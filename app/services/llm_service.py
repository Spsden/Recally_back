
import time

def transcribe_audio(file_path: str):
    """Dummy function to simulate audio transcription."""
    print(f"Transcribing {file_path}...")
    time.sleep(2) # Simulate network latency
    return "This is a dummy transcription of the audio file."

def summarize_text(text: str):
    """Dummy function to simulate text summarization."""
    print(f"Summarizing text: '{text[:50]}...' ")
    time.sleep(1)
    return "This is a dummy summary.", ["dummy", "tag"], [{"type": "reminder", "title": "Dummy reminder", "datetime": "2025-07-18T10:00:00"}]

def ocr_image(file_path: str):
    """Dummy function to simulate image OCR."""
    print(f"Performing OCR on {file_path}...")
    time.sleep(2)
    return "This is dummy text extracted from the image."
