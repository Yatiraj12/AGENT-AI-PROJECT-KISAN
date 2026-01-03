from PIL import Image
from typing import Tuple


def load_image(image_path: str) -> Image.Image:
    return Image.open(image_path).convert("RGB")


def resize_image(
    image: Image.Image,
    size: Tuple[int, int] = (224, 224)
) -> Image.Image:
    return image.resize(size)
