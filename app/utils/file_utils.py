import os
from typing import List


ALLOWED_IMAGE_EXTENSIONS: List[str] = [".jpg", ".jpeg", ".png"]


def is_allowed_file(filename: str) -> bool:
    _, ext = os.path.splitext(filename.lower())
    return ext in ALLOWED_IMAGE_EXTENSIONS


def ensure_directory(path: str) -> None:
    if not os.path.exists(path):
        os.makedirs(path)


def save_uploaded_file(file_bytes: bytes, save_path: str) -> None:
    with open(save_path, "wb") as f:
        f.write(file_bytes)
