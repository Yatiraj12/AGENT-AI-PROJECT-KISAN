from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
import traceback

from app.api.routes import router as disease_router


def create_app() -> FastAPI:
    app = FastAPI(
        title="Crop Disease AI Agent",
        description="AI-based crop disease detection and advisory system",
        version="1.0.0"
    )

    # -------------------------
    # CORS (UNCHANGED)
    # -------------------------
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # -------------------------
    # GLOBAL EXCEPTION HANDLER (NEW)
    # -------------------------
    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=500,
            content={
                "error": str(exc),
                "trace": traceback.format_exc()
            }
        )

    # -------------------------
    # Serve frontend (UNCHANGED)
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
    # Routers (UNCHANGED)
    # -------------------------
    app.include_router(disease_router)

    # -------------------------
    # Health check (UNCHANGED)
    # -------------------------
    @app.get("/health")
    def health_check():
        return {
            "status": "ok",
            "service": "crop-disease-ai-agent"
        }

    return app


app = create_app()
