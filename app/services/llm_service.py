import os
from typing import List, Dict, Any

from groq import Groq
from dotenv import load_dotenv


# Load environment variables from .env at startup
load_dotenv()


class LLMService:
    """
    Groq LLM abstraction layer.
    """

    def __init__(self, model: str = None):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise RuntimeError(
                "GROQ_API_KEY is not set. "
                "Please add it to your .env file or environment variables."
            )

        self.client = Groq(api_key=api_key)
        self.model = model or os.getenv("GROQ_MODEL", "qwen/qwen3-32b")

    def generate(self, messages: List[Dict[str, str]]) -> Dict[str, Any]:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.2
        )

        content = response.choices[0].message.content
        return self._safe_parse(content)

    def _safe_parse(self, content: str) -> Dict[str, Any]:
        """
        Ensures model output is always usable by agents.
        """

        try:
            import json
            return json.loads(content)
        except Exception:
            return {
                "raw_response": content
            }
