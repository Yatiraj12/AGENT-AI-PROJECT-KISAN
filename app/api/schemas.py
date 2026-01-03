from typing import Dict, Any, List, Optional
from pydantic import BaseModel


class DiseaseAnalysisRequest(BaseModel):
    crop: str
    visual_features: Dict[str, Any]
    language: Optional[str] = "en"
    # Supported examples: "en", "kn", "hi"


class SeverityResponse(BaseModel):
    severity_percent: float
    risk_level: str


class DiseaseResponse(BaseModel):
    disease: str
    confidence: float
    explanation: Optional[str] = None


class SolutionResponse(BaseModel):
    treatment: List[str]
    prevention: List[str]


class DiseaseAnalysisResponse(BaseModel):
    crop: str
    disease: DiseaseResponse
    severity: SeverityResponse
    solution: SolutionResponse
