from typing import Dict, Any
from app.services.llm_service import LLMService


class DiseaseAgent:
    def __init__(self, llm_service: LLMService = None):
        self.llm_service = llm_service

    def detect_disease(self, crop: str, visual_features: Dict[str, Any]) -> Dict[str, Any]:
        base_result = self._detect_with_rules(crop, visual_features)

        if not self.llm_service:
            return base_result

        explanation = self._get_llm_explanation(
            crop=crop,
            visual_features=visual_features,
            disease=base_result["disease"]
        )

        base_result["explanation"] = explanation
        return base_result

    def _detect_with_rules(self, crop: str, visual_features: Dict[str, Any]) -> Dict[str, Any]:
        color = visual_features.get("leaf_color", "").lower()
        spots = visual_features.get("spots", "").lower()

        if crop.lower() == "tomato":
            if "brown" in spots and "circular" in spots:
                return {"disease": "Early Blight", "confidence": 0.75}
            if "yellow" in color and "mosaic" in spots:
                return {"disease": "Tomato Mosaic Virus", "confidence": 0.65}

        return {"disease": "Healthy or Unknown", "confidence": 0.4}

    def _get_llm_explanation(
        self,
        crop: str,
        visual_features: Dict[str, Any],
        disease: str
    ) -> str:

        messages = [
            {
                "role": "system",
                "content": (
                    "You are an agricultural expert. "
                    "Explain plant diseases clearly for farmers."
                )
            },
            {
                "role": "user",
                "content": (
                    f"Crop: {crop}\n"
                    f"Detected disease: {disease}\n"
                    f"Observed features: {visual_features}\n\n"
                    "Explain why this disease is likely, in simple language."
                )
            }
        ]

        response = self.llm_service.generate(messages)
        return response.get("raw_response", "")
