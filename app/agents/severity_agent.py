from typing import Dict, Any


class SeverityAgent:
    def estimate_severity(self, visual_features: Dict[str, Any]) -> Dict[str, Any]:
        """
        Estimate disease severity based on affected leaf area.

        Args:
            visual_features: Extracted image features

        Returns:
            Dict with severity percentage and risk level
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
