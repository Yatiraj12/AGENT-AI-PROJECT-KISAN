from typing import Dict, Any
from PIL import Image
import numpy as np


class ImagePreprocessor:
    """
    Extracts basic visual signals from an image.
    This does not perform ML-based vision.
    """

    def preprocess(self, image_path: str) -> Dict[str, Any]:
        image = Image.open(image_path).convert("RGB")
        image_array = np.array(image)

        avg_color = image_array.mean(axis=(0, 1))

        leaf_color = self._infer_leaf_color(avg_color)

        visual_features = {
            "leaf_color": leaf_color,
            "spots": "unknown",
            "texture": "unknown",
            "affected_area_percent": self._estimate_affected_area(image_array)
        }

        return visual_features

    def _infer_leaf_color(self, avg_color) -> str:
        r, g, b = avg_color

        if g > r and g > b:
            return "green"
        if r > g and r > b:
            return "brown"
        if g > 150 and r > 150:
            return "yellow"

        return "unknown"

    def _estimate_affected_area(self, image_array: np.ndarray) -> float:
        gray = image_array.mean(axis=2)
        threshold = gray.mean() * 0.8
        affected_pixels = (gray < threshold).sum()
        total_pixels = gray.size

        return round((affected_pixels / total_pixels) * 100, 2)
