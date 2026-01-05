from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router as disease_router


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

    # Routers
    app.include_router(disease_router)

    # Root endpoint (IMPORTANT for Wasmer / health checks)
    @app.get("/")
    def root():
        return {"message": "Crop Disease AI Agent running"}

    @app.get("/health")
    def health_check():
        return {
            "status": "ok",
            "service": "crop-disease-ai-agent"
        }

    return app


app = create_app()
