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
# Translation helpers (RE-ENABLED ✅)
# -------------------------------------------------
def translate_text(text: str, language: str) -> str:
    if not text or language == "en":
        return text

    messages = [
        {
            "role": "system",
            "content": "You are an agricultural expert translating content for farmers."
        },
        {
            "role": "user",
            "content": (
                f"Translate the following agricultural explanation into {language}. "
                f"Keep it simple and farmer-friendly:\n\n{text}"
            )
        }
    ]

    response = llm_service.generate(messages)
    return response.get("raw_response", text)


def translate_list(items: list[str], language: str) -> list[str]:
    if not items or language == "en":
        return items

    joined_text = "\n".join(f"- {item}" for item in items)

    messages = [
        {
            "role": "system",
            "content": "You are translating agricultural instructions for farmers."
        },
        {
            "role": "user",
            "content": (
                f"Translate the following steps into {language}. "
                f"Keep them clear and actionable:\n\n{joined_text}"
            )
        }
    ]

    response = llm_service.generate(messages)
    translated_text = response.get("raw_response", joined_text)

    return [
        line.strip("- ").strip()
        for line in translated_text.split("\n")
        if line.strip()
    ]


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

    # Save image safely
    try:
        file_bytes = await file.read()
        save_uploaded_file(file_bytes, file_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Image save failed: {str(e)}")

    # TEMP visual features (working)
    visual_features = {
        "leaf_color": "green",
        "spots": "yes",
        "texture": "rough"
    }

    disease_result = disease_agent.detect_disease(
        crop=crop,
        visual_features=visual_features
    )

    # ✅ TRANSLATE EXPLANATION
    disease_result["explanation"] = translate_text(
        disease_result.get("explanation"),
        language
    )

    severity_result = severity_agent.estimate_severity(
        visual_features=visual_features
    )

    solution_result = solution_agent.recommend_solution(
        crop=crop,
        disease=disease_result["disease"],
        severity_info=severity_result
    )

    # ✅ TRANSLATE SOLUTION
    solution_result["treatment"] = translate_list(
        solution_result.get("treatment", []),
        language
    )

    solution_result["prevention"] = translate_list(
        solution_result.get("prevention", []),
        language
    )

    return DiseaseAnalysisResponse(
        crop=crop,
        disease=DiseaseResponse(**disease_result),
        severity=SeverityResponse(**severity_result),
        solution=SolutionResponse(**solution_result)
    )
