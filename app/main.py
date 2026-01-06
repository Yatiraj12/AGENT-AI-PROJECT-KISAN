from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.api.routes import router as disease_router


def create_app() -> FastAPI:
    app = FastAPI(
        title="Crop Disease AI Agent",
        description="AI-based crop disease detection and advisory system",
        version="1.0.0"
    )

    # -------------------------
    # CORS (keep as-is)
    # -------------------------
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # -------------------------
    # Serve frontend (NEW)
    # -------------------------
    app.mount(
        "/static",
        StaticFiles(directory="frontend"),
        name="static"
    )

    @app.get("/")
    def serve_frontend():
        return FileResponse("frontend/index.html")

    # -------------------------
    # Routers (keep as-is)
    # -------------------------
    app.include_router(disease_router)

    # -------------------------
    # Health check (keep as-is)
    # -------------------------
    @app.get("/health")
    def health_check():
        return {
            "status": "ok",
            "service": "crop-disease-ai-agent"
        }

    return app


app = create_app()
