from typing import Dict, Any


def format_analysis_response(
    crop: str,
    disease: Dict[str, Any],
    severity: Dict[str, Any],
    solution: Dict[str, Any]
) -> Dict[str, Any]:
    return {
        "crop": crop,
        "disease": {
            "name": disease.get("disease"),
            "confidence": disease.get("confidence")
        },
        "severity": {
            "percentage": severity.get("severity_percent"),
            "risk_level": severity.get("risk_level")
        },
        "solution": {
            "treatment": solution.get("treatment", []),
            "prevention": solution.get("prevention", [])
        }
    }
