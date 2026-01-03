import json
from pathlib import Path


DATA_DIR = Path("data")
MODEL_STORE = Path("models_store")


def load_training_data():
    """
    Load training metadata.
    This function can later be replaced with real dataset loaders.
    """

    sample_data = [
        {
            "crop": "Tomato",
            "features": {
                "leaf_color": "yellow-green",
                "spots": "dark brown circular spots",
                "affected_area_percent": 45
            },
            "label": "Early Blight"
        },
        {
            "crop": "Tomato",
            "features": {
                "leaf_color": "yellow",
                "spots": "mosaic pattern",
                "affected_area_percent": 30
            },
            "label": "Tomato Mosaic Virus"
        }
    ]

    return sample_data


def train():
    print("Starting training pipeline")

    training_data = load_training_data()

    MODEL_STORE.mkdir(exist_ok=True)

    labels = sorted({item["label"] for item in training_data})

    labels_path = MODEL_STORE / "labels.txt"
    with open(labels_path, "w") as f:
        for label in labels:
            f.write(label + "\n")

    model_metadata = {
        "model_type": "rule_based_placeholder",
        "num_samples": len(training_data),
        "labels": labels
    }

    metadata_path = MODEL_STORE / "model_metadata.json"
    with open(metadata_path, "w") as f:
        json.dump(model_metadata, f, indent=2)

    print("Training completed")
    print(f"Labels saved to {labels_path}")
    print(f"Metadata saved to {metadata_path}")


if __name__ == "__main__":
    train()
