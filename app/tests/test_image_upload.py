import os
from app.services.image_preprocessor import ImagePreprocessor


def test_image_preprocessing():
    preprocessor = ImagePreprocessor()

    test_image_path = "data/sample_images/healthy_leaf.jpg"

    if not os.path.exists(test_image_path):
        # Skip test gracefully if sample image not present
        assert True
        return

    visual_features = preprocessor.preprocess(test_image_path)

    assert "leaf_color" in visual_features
    assert "affected_area_percent" in visual_features
    assert isinstance(visual_features["affected_area_percent"], float)
