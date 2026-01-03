from app.services.llm_service import LLMService


class TranslationService:
    def __init__(self, llm_service: LLMService):
        self.llm_service = llm_service

    def translate(self, text: str, target_language: str) -> str:
        if target_language == "en":
            return text

        messages = [
            {
                "role": "system",
                "content": "You are a professional agricultural translator."
            },
            {
                "role": "user",
                "content": (
                    f"Translate the following agricultural explanation into {target_language}. "
                    f"Keep meaning accurate and farmer-friendly:\n\n{text}"
                )
            }
        ]

        response = self.llm_service.generate(messages)
        return response.get("raw_response", text)
