"""ADSNPP FastAPI gateway.

Run with:
    uvicorn adsnpp.api.gateway:create_app --factory --host 0.0.0.0 --port 8000 --reload
"""

from __future__ import annotations

from fastapi import FastAPI

from adsnpp import __version__
from adsnpp.circular.ncef_engine import NCEFScoringEngine


def create_app() -> FastAPI:
    app = FastAPI(
        title="ADSNPP API",
        description="Algorithmic Decision System for Nuclear Power Plants",
        version=__version__,
        docs_url="/api/docs",
    )

    @app.get("/api/health")
    def health() -> dict[str, str]:
        return {"status": "ok", "version": __version__}

    @app.post("/api/ncef/compare")
    def ncef_compare(technologies: dict[str, dict[str, float]]) -> list[dict[str, float | str]]:
        engine = NCEFScoringEngine()
        results = engine.compare_technologies(technologies)
        return [
            {"technology": r.technology, "adjusted_cei": r.adjusted_cei} for r in results
        ]

    return app
