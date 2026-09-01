"""Kayock Local AI Trophy Room — contest showcase dashboard."""

from __future__ import annotations

import sys
from pathlib import Path

# Ensure repo root on path for governor imports
REPO_ROOT = Path(__file__).resolve().parent.parent
TROPHY_ROOM_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(REPO_ROOT))
sys.path.insert(0, str(TROPHY_ROOM_ROOT))

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from adapters.evidence import load_evidence_vault, load_milestones
from adapters.governor_data import get_governor_panel
from adapters.services import probe_all_services, services_to_dict
from adapters.telemetry import get_gpu_summary
from config import (
    HANDOFF_TIMELINE,
    HOST,
    LEMONADE_MODEL,
    POLL_INTERVAL_MS,
    PORT,
    TROPHY_ROOM_ROOT,
    VERIFIED_BENCHMARK,
    VERIFIED_THROUGHPUT,
)

app = FastAPI(title="Kayock Local AI Trophy Room", version="0.1.0")

static_dir = TROPHY_ROOM_ROOT / "static"
templates_dir = TROPHY_ROOM_ROOT / "templates"
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")
templates = Jinja2Templates(directory=str(templates_dir))
templates.env.cache_size = 0  # avoid unhashable context in template cache (Py 3.14)


@app.get("/", response_class=HTMLResponse)
async def index(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        request,
        "index.html",
        {
            "poll_ms": POLL_INTERVAL_MS,
            "model": LEMONADE_MODEL,
            "milestones": load_milestones(),
            "handoff_timeline": HANDOFF_TIMELINE,
            "throughput": VERIFIED_THROUGHPUT,
            "benchmark": VERIFIED_BENCHMARK,
            "evidence": load_evidence_vault(),
            "governor": get_governor_panel(),
            "services": services_to_dict(probe_all_services()),
        },
    )


@app.get("/api/status")
async def api_status() -> JSONResponse:
    services = probe_all_services()
    gpu = get_gpu_summary()
    lemon = next((s for s in services if s.id == "lemonade"), None)
    ff = next((s for s in services if s.id == "father_fox"), None)
    gov = next((s for s in services if s.id == "governor"), None)

    return JSONResponse({
        "lemonade": {
            "status": lemon.status if lemon else "unknown",
            "online": lemon.status == "online" if lemon else False,
            "model": LEMONADE_MODEL,
            "details": lemon.details if lemon else {},
        },
        "gpu": gpu,
        "father_fox": {"status": ff.status if ff else "unknown"},
        "governor": {"status": gov.status if gov else "unknown"},
        "rvc_handoff": {"badge": "VERIFIED", "status": "documented"},
        "optimization": {
            "improvement_pct": VERIFIED_THROUGHPUT["improvement_pct"],
            "badge": "VERIFIED",
        },
        "services": services_to_dict(services),
    })


@app.get("/api/evidence")
async def api_evidence() -> JSONResponse:
    return JSONResponse({"items": load_evidence_vault()})


@app.get("/api/governor")
async def api_governor() -> JSONResponse:
    return JSONResponse(get_governor_panel())


def main() -> None:
    import uvicorn
    print(f"Trophy Room listening on http://{HOST}:{PORT}")
    if HOST == "0.0.0.0":
        print("LAN mode: dashboard reachable from other devices on this network.")
    uvicorn.run(app, host=HOST, port=PORT, log_level="info")


if __name__ == "__main__":
    main()
