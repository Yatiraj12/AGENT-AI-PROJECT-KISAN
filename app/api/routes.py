from fastapi import APIRouter, HTTPException, UploadFile, File, Form
import os
import uuid

from app.api.schemas import (
    DiseaseAnalysisRequest,
    DiseaseAnalysisResponse,
    DiseaseResponse,
    SeverityResponse,
    SolutionResponse,
)

from app.agents.disease_agent import DiseaseAgent
from app.agents.severity_agent import SeverityAgent
from app.agents.solution_agent import SolutionAgent

from app.services.image_preprocessor import ImagePreprocessor
from app.services.llm_service import LLMService

from app.utils.file_utils import (
    is_allowed_file,
    ensure_directory,
    save_uploaded_file
)

from app.utils.db import SessionLocal
from app.models.history_model import AnalysisHistory


router = APIRouter(prefix="/analyze", tags=["Crop Disease Analysis"])


# -------------------------------------------------
# Knowledge Base (UNCHANGED)
# -------------------------------------------------
knowledge_base = {
    "Early Blight": {
        "treatment": [
            "Remove infected leaves",
            "Apply copper-based fungicide"
        ],
        "advanced_treatment": [
            "Use chlorothalonil fungicide"
        ],
        "prevention": [
            "Avoid overhead irrigation",
            "Practice crop rotation"
        ]
    },
    "Tomato Mosaic Virus": {
        "treatment": [
            "Remove infected plants"
        ],
        "advanced_treatment": [],
        "prevention": [
            "Use resistant seed varieties",
            "Disinfect tools regularly"
        ]
    }
}

# -------------------------------------------------
# Services & Agents (UNCHANGED)
# -------------------------------------------------
llm_service = LLMService()

disease_agent = DiseaseAgent(llm_service=llm_service)
severity_agent = SeverityAgent()
solution_agent = SolutionAgent(
    knowledge_base=knowledge_base,
    llm_service=llm_service
)

image_preprocessor = ImagePreprocessor()


# -------------------------------------------------
# Upload configuration (UNCHANGED)
# -------------------------------------------------
UPLOAD_DIR = "/tmp/uploads"
ensure_directory(UPLOAD_DIR)


# -------------------------------------------------
# History persistence helper (UNCHANGED)
# -------------------------------------------------
def save_history(
    crop: str,
    disease_result: dict,
    severity_result: dict,
    image_path: str | None = None
):
    db = SessionLocal()
    try:
        record = AnalysisHistory(
            crop=crop,
            disease=disease_result.get("disease"),
            confidence=disease_result.get("confidence"),
            severity_percent=severity_result.get("severity_percent"),
            risk_level=severity_result.get("risk_level"),
            explanation=disease_result.get("explanation"),
            image_path=image_path
        )
        db.add(record)
        db.commit()
    finally:
        db.close()


# =================================================
# IMAGE UPLOAD ANALYSIS
# =================================================
@router.post("/image", response_model=DiseaseAnalysisResponse)
async def analyze_disease_from_image(
    crop: str = Form(...),
    language: str = Form("en"),
    file: UploadFile = File(...)
):

    if not is_allowed_file(file.filename):
        raise HTTPException(status_code=400, detail="Invalid image format")

    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)

    # -------------------------
    # SAFE FILE SAVE (UNCHANGED)
    # -------------------------
    try:
        file_bytes = await file.read()
        save_uploaded_file(file_bytes, file_path)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Image save failed: {str(e)}"
        )

    # -------------------------------------------------
    # 🔴 UPDATE 1: BYPASS IMAGE PREPROCESSOR (TEMP)
    # -------------------------------------------------
    visual_features = {
        "leaf_color": "green",
        "spots": True,
        "texture": "rough"
    }

    disease_result = disease_agent.detect_disease(
        crop=crop,
        visual_features=visual_features
    )

    severity_result = severity_agent.estimate_severity(
        visual_features=visual_features
    )

    solution_result = solution_agent.recommend_solution(
        crop=crop,
        disease=disease_result["disease"],
        severity_info=severity_result
    )

    # -------------------------------------------------
    # 🔴 UPDATE 2: DISABLE DB SAVE (TEMP)
    # -------------------------------------------------
    # save_history(
    #     crop=crop,
    #     disease_result=disease_result,
    #     severity_result=severity_result,
    #     image_path=file_path
    # )

    return DiseaseAnalysisResponse(
        crop=crop,
        disease=DiseaseResponse(**disease_result),
        severity=SeverityResponse(**severity_result),
        solution=SolutionResponse(**solution_result)
    )
