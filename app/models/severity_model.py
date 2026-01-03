from typing import Dict, Any


class SeverityModel:
    """
    Severity estimation model based on affected area percentage.
    """

    def predict(self, visual_features: Dict[str, Any]) -> Dict[str, Any]:
        """
        Predict severity percentage and risk level.

        Args:
            visual_features: High-level visual features

        Returns:
            Dict with severity_percent and risk_level
        """

        coverage = visual_features.get("affected_area_percent", 0)

        if coverage < 10:
            risk = "Low"
        elif coverage < 30:
            risk = "Moderate"
        elif coverage < 60:
            risk = "High"
        else:
            risk = "Critical"

        return {
            "severity_percent": coverage,
            "risk_level": risk
        }
