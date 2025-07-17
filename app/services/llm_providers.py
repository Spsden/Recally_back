
import openai
from app.config import settings

class BaseProvider:
    def __init__(self, api_key=None, base_url=None):
        self.api_key = api_key
        self.base_url = base_url

    def transcribe(self, file_path: str):
        raise NotImplementedError

    def summarize(self, text: str):
        raise NotImplementedError

    def ocr(self, image_path: str):
        raise NotImplementedError

class OpenAIProvider(BaseProvider):
    def __init__(self, api_key=None, base_url=None):
        super().__init__(api_key, base_url)
        self.client = openai.OpenAI(api_key=self.api_key, base_url=self.base_url)

    def transcribe(self, file_path: str):
        with open(file_path, "rb") as audio_file:
            transcription = self.client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )
        return transcription.text

    def summarize(self, text: str):
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes text."},
                {"role": "user", "content": f"Summarize the following text:

{text}"}
            ]
        )
        return response.choices[0].message.content

    def ocr(self, image_path: str):
        # GPT-4 Vision for OCR
        # This is a simplified example. You might need to handle image encoding differently.
        response = self.client.chat.completions.create(
            model="gpt-4-vision-preview",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Extract the text from this image."},
                        {
                            "type": "image_url",
                            "image_url": f"data:image/jpeg;base64,{image_path}",
                        },
                    ],
                }
            ],
            max_tokens=300,
        )
        return response.choices[0].message.content

class OllamaProvider(BaseProvider):
    def __init__(self, base_url="http://localhost:11434/api"):
        super().__init__(base_url=base_url)
        # Ollama doesn't require an API key
        self.client = openai.OpenAI(base_url=self.base_url, api_key="ollama")

    def summarize(self, text: str):
        response = self.client.chat.completions.create(
            model="llama2", # Or any other model you have pulled
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes text."},
                {"role": "user", "content": f"Summarize the following text:

{text}"}
            ]
        )
        return response.choices[0].message.content
    
    def transcribe(self, file_path: str):
        # Ollama doesn't have a direct audio transcription API in the same way as OpenAI.
        # This would require a custom solution or a different library.
        # For now, we'll return a placeholder.
        return "Transcription not supported by Ollama provider in this implementation."

    def ocr(self, image_path: str):
        # This would require a model like llava
        return "OCR not supported by Ollama provider in this implementation."


class GroqProvider(BaseProvider):
    def __init__(self, api_key):
        super().__init__(api_key=api_key, base_url="https://api.groq.com/openai/v1")
        self.client = openai.OpenAI(api_key=self.api_key, base_url=self.base_url)

    def summarize(self, text: str):
        response = self.client.chat.completions.create(
            model="llama3-8b-8192", # Or other supported models
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes text."},
                {"role": "user", "content": f"Summarize the following text:

{text}"}
            ]
        )
        return response.choices[0].message.content

    def transcribe(self, file_path: str):
        with open(file_path, "rb") as audio_file:
            transcription = self.client.audio.transcriptions.create(
                model="whisper-large-v3",
                file=audio_file
            )
        return transcription.text

    def ocr(self, image_path: str):
        return "OCR not supported by Groq provider."


class LLMService:
    def __init__(self):
        provider_name = settings.LLM_PROVIDER.lower()
        if provider_name == "openai":
            self.provider = OpenAIProvider(api_key=settings.OPENAI_API_KEY)
        elif provider_name == "ollama":
            self.provider = OllamaProvider(base_url=settings.OLLAMA_BASE_URL)
        elif provider_name == "groq":
            self.provider = GroqProvider(api_key=settings.GROQ_API_KEY)
        else:
            raise ValueError(f"Unsupported LLM provider: {provider_name}")

    def transcribe_audio(self, file_path: str):
        return self.provider.transcribe(file_path)

    def summarize_text(self, text: str):
        return self.provider.summarize(text)

    def ocr_image(self, image_path: str):
        return self.provider.ocr(image_path)

llm_service = LLMService()
