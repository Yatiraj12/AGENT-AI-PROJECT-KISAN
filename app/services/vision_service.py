from typing import Dict, Any
from app.services.llm_service import LLMService


class VisionService:
    """
    Vision reasoning using Groq LLM.
    Converts visual features into meaningful observations.
    """

    def __init__(self, llm_service: LLMService = None):
        self.llm_service = llm_service or LLMService()

    def analyze(self, crop: str, visual_features: Dict[str, Any]) -> Dict[str, Any]:
        system_prompt = {
            "role": "system",
            "content": (
                "You are an agricultural vision analysis expert. "
                "You interpret plant leaf conditions based on extracted visual features."
            )
        }

        user_prompt = {
            "role": "user",
            "content": (
                f"Crop: {crop}\n"
                f"Extracted visual features: {visual_features}\n"
                "Infer visible symptoms in structured JSON with keys: "
                "leaf_color, spots, texture, affected_area_percent."
            )
        }

        response = self.llm_service.generate([system_prompt, user_prompt])

        return self._normalize_response(response, visual_features)

    def _normalize_response(
        self,
        response: Dict[str, Any],
        fallback_features: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Guarantees downstream compatibility.
        """

        return {
            "leaf_color": response.get("leaf_color", fallback_features.get("leaf_color")),
            "spots": response.get("spots", fallback_features.get("spots", "unknown")),
            "texture": response.get("texture", fallback_features.get("texture", "unknown")),
            "affected_area_percent": response.get(
                "affected_area_percent",
                fallback_features.get("affected_area_percent", 0)
            )
        }
