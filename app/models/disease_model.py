from typing import Dict, Any


class DiseaseModel:
    """
    Disease inference model abstraction.
    Can be backed by rules, ML, or LLM-based reasoning.
    """

    def predict(self, crop: str, visual_features: Dict[str, Any]) -> Dict[str, Any]:
        """
        Predict disease name and confidence.

        Args:
            crop: Crop name
            visual_features: High-level visual features

        Returns:
            Dict with disease and confidence
        """

        crop = crop.lower()
        color = visual_features.get("leaf_color", "").lower()
        spots = visual_features.get("spots", "").lower()

        if crop == "tomato":
            if "brown" in spots and "circular" in spots:
                return {"disease": "Early Blight", "confidence": 0.75}
            if "yellow" in color and "mosaic" in spots:
                return {"disease": "Tomato Mosaic Virus", "confidence": 0.65}

        return {"disease": "Healthy or Unknown", "confidence": 0.4}
