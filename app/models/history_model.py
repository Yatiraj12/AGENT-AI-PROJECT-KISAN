from sqlalchemy import Column, Integer, String, Float, Text
from app.utils.db import Base


class AnalysisHistory(Base):
    __tablename__ = "analysis_history"

    id = Column(Integer, primary_key=True, index=True)
    crop = Column(String, index=True)
    disease = Column(String)
    confidence = Column(Float)
    severity_percent = Column(Float)
    risk_level = Column(String)
    explanation = Column(Text)
    image_path = Column(String, nullable=True)
