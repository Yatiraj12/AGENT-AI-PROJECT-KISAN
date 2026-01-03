from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router as disease_router
from app.utils.db import engine, Base


def create_app() -> FastAPI:
    app = FastAPI(
        title="Crop Disease AI Agent",
        description="AI-based crop disease detection and advisory system",
        version="1.0.0"
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # 🔥 THIS IS THE KEY LINE
    Base.metadata.create_all(bind=engine)

    app.include_router(disease_router)

    @app.get("/health")
    def health_check():
        return {
            "status": "ok",
            "service": "crop-disease-ai-agent"
        }

    return app


app = create_app()
