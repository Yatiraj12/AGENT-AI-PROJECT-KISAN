from app.agents.disease_agent import DiseaseAgent


def test_detect_disease_early_blight():
    agent = DiseaseAgent()

    visual_features = {
        "leaf_color": "yellow-green",
        "spots": "dark brown circular spots",
        "affected_area_percent": 45
    }

    result = agent.detect_disease(
        crop="Tomato",
        visual_features=visual_features
    )

    assert result["disease"] == "Early Blight"
    assert result["confidence"] > 0.5


def test_detect_unknown_disease():
    agent = DiseaseAgent()

    visual_features = {
        "leaf_color": "green",
        "spots": "none",
        "affected_area_percent": 2
    }

    result = agent.detect_disease(
        crop="Tomato",
        visual_features=visual_features
    )

    assert "disease" in result
    assert "confidence" in result
