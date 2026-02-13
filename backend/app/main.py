"""FastAPI application for AlphaGenome Viewer."""

import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from app.config import PLOTS_DIR
from app.routers import config, metadata, predictions, variants

app = FastAPI(
    title="AlphaGenome Viewer API",
    version="1.0.0",
    description="API for AlphaGenome genomic predictions",
)

# CORS middleware — configurable via $CORS_ORIGINS (comma-separated)
cors_origins = os.environ.get("CORS_ORIGINS", "http://localhost:5173").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure plots directory exists and mount static files
os.makedirs(PLOTS_DIR, exist_ok=True)
app.mount("/plots", StaticFiles(directory=PLOTS_DIR), name="plots")

# Include routers
app.include_router(metadata.router, prefix="/api/metadata", tags=["metadata"])
app.include_router(predictions.router, prefix="/api/predict", tags=["predictions"])
app.include_router(variants.router, prefix="/api", tags=["variants"])
app.include_router(config.router, prefix="/api/config", tags=["config"])


@app.get("/health")
def health():
    """Health check endpoint."""
    return {"status": "ok"}


@app.exception_handler(Exception)
async def generic_exception_handler(request, exc):
    """Handle unexpected errors."""
    return JSONResponse(
        status_code=500,
        content={"error": str(exc), "type": "internal_error"},
    )


# Serve built frontend (only when FRONTEND_DIST_DIR is explicitly set — containers only)
FRONTEND_DIR = os.environ.get("FRONTEND_DIST_DIR", "")

if FRONTEND_DIR and os.path.isdir(FRONTEND_DIR):
    assets_dir = os.path.join(FRONTEND_DIR, "assets")
    if os.path.isdir(assets_dir):
        app.mount("/assets", StaticFiles(directory=assets_dir), name="frontend-assets")

    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        """Serve the SPA frontend, falling back to index.html for client-side routing."""
        file_path = os.path.join(FRONTEND_DIR, full_path)
        if full_path and os.path.isfile(file_path):
            return FileResponse(file_path)
        return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))
