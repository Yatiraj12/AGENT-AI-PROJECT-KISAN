from typing import Dict, Any


class ImageClassifier:
    """
    Lightweight image classification abstraction.
    This class assumes image preprocessing has already occurred
    and works on extracted numeric or textual features.
    """

    def classify(self, image_features: Dict[str, Any]) -> Dict[str, Any]:
        """
        Classify image features into interpretable visual attributes.

        Args:
            image_features: Raw extracted features from image processing

        Returns:
            Dict of high-level visual features
        """

        classified_features = {
            "leaf_color": image_features.get("leaf_color", "unknown"),
            "spots": image_features.get("spots", "none"),
            "texture": image_features.get("texture", "normal"),
            "affected_area_percent": image_features.get("affected_area_percent", 0)
        }

        return classified_features
