from app.agents.severity_agent import SeverityAgent


def test_low_severity():
    agent = SeverityAgent()

    visual_features = {
        "affected_area_percent": 5
    }

    result = agent.estimate_severity(visual_features)

    assert result["risk_level"] == "Low"
    assert result["severity_percent"] == 5


def test_high_severity():
    agent = SeverityAgent()

    visual_features = {
        "affected_area_percent": 55
    }

    result = agent.estimate_severity(visual_features)

    assert result["risk_level"] == "High"
    assert result["severity_percent"] == 55
