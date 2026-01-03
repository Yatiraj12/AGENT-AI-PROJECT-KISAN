from app.models.disease_model import DiseaseModel
from app.models.severity_model import SeverityModel


def load_evaluation_data():
    return [
        {
            "crop": "Tomato",
            "features": {
                "leaf_color": "yellow-green",
                "spots": "dark brown circular spots",
                "affected_area_percent": 50
            },
            "expected_disease": "Early Blight"
        },
        {
            "crop": "Tomato",
            "features": {
                "leaf_color": "yellow",
                "spots": "mosaic pattern",
                "affected_area_percent": 20
            },
            "expected_disease": "Tomato Mosaic Virus"
        }
    ]


def evaluate():
    disease_model = DiseaseModel()
    severity_model = SeverityModel()

    evaluation_data = load_evaluation_data()

    correct = 0

    for sample in evaluation_data:
        prediction = disease_model.predict(
            crop=sample["crop"],
            visual_features=sample["features"]
        )

        severity = severity_model.predict(
            visual_features=sample["features"]
        )

        is_correct = prediction["disease"] == sample["expected_disease"]
        correct += int(is_correct)

        print("Input:", sample["features"])
        print("Predicted Disease:", prediction)
        print("Severity:", severity)
        print("Expected Disease:", sample["expected_disease"])
        print("Result:", "Correct" if is_correct else "Incorrect")
        print("-" * 40)

    accuracy = correct / len(evaluation_data)
    print(f"Evaluation Accuracy: {accuracy:.2f}")


if __name__ == "__main__":
    evaluate()
