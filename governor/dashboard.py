"""Lightweight local web dashboard."""

from __future__ import annotations

import html

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from governor.config import DASHBOARD_HOST, DASHBOARD_PORT, LEMONADE_MODEL
from governor.handoff import observe_handoff
from governor.lemonade import check_lemonade
from governor.persistence import (
    get_latest_benchmark,
    get_recent_decisions,
    get_recent_events,
    get_saved_profile,
    init_db,
)
from governor.telemetry import collect_telemetry, format_metric


def create_app() -> FastAPI:
    init_db()
    app = FastAPI(title="Kayock AI Resource Governor", version="0.1.0")

    @app.get("/", response_class=HTMLResponse)
    def index() -> str:
        telem = collect_telemetry()
        lemonade = check_lemonade()
        handoff = observe_handoff(telemetry=telem)
        latest = get_latest_benchmark()
        saved = get_saved_profile("LOW_LATENCY")
        events = get_recent_events(10)
        decisions = get_recent_decisions(10)

        gpu = telem.gpu
        rows = [
            ("Name", format_metric(gpu.name)),
            ("Utilization %", format_metric(gpu.utilization_percent)),
            ("VRAM used (MiB)", format_metric(gpu.vram_used_mib)),
            ("VRAM free (MiB)", format_metric(gpu.vram_free_mib)),
            ("Temperature °C", format_metric(gpu.temperature_c)),
            ("Clock (MHz)", format_metric(gpu.clock_graphics_mhz)),
            ("Power draw (W)", format_metric(gpu.power_draw_w)),
            ("Throttle", format_metric(gpu.throttle_reasons)),
        ]

        gpu_html = "".join(
            f"<tr><td>{html.escape(k)}</td><td>{html.escape(v)}</td></tr>"
            for k, v in rows
        )

        lemon_status = "online" if lemonade.online else "offline"
        if not lemonade.authenticated:
            lemon_status += " (no API key)"

        opt_html = "<p>No benchmark runs yet.</p>"
        if latest:
            opt_html = f"""
            <p>Last run: {html.escape(latest['run_id'])}</p>
            <p>Profile: {html.escape(latest['profile_name'])}</p>
            <p>Score: {latest.get('score', 'n/a')}</p>
            """
        if saved:
            opt_html += f"<p>Best LOW_LATENCY profile score: {saved.get('score')}</p>"

        events_html = "".join(
            f"<li><code>{html.escape(e['timestamp'])}</code> "
            f"[{html.escape(e['event_type'])}] {html.escape(e['message'])}</li>"
            for e in events
        ) or "<li>None</li>"

        decisions_html = "".join(
            f"<li><code>{html.escape(d['timestamp'])}</code> "
            f"{html.escape(d['decision'])} — {html.escape(d['reason'])}</li>"
            for d in decisions
        ) or "<li>None</li>"

        return f"""<!DOCTYPE html>
<html><head>
<meta charset="utf-8"><title>Kayock AI Resource Governor</title>
<style>
body {{ font-family: system-ui, sans-serif; margin: 24px; background: #111; color: #eee; }}
h1 {{ font-size: 1.4rem; }}
section {{ background: #1c1c1c; padding: 16px; margin: 12px 0; border-radius: 8px; }}
table {{ border-collapse: collapse; width: 100%; }}
td, th {{ border: 1px solid #333; padding: 6px 10px; text-align: left; }}
code {{ font-size: 0.85rem; }}
</style></head><body>
<h1>KAYOCK AI RESOURCE GOVERNOR</h1>

<section><h2>GPU</h2>
<table>{gpu_html}</table>
<p>CPU: {format_metric(telem.system.cpu_percent)}% |
RAM: {format_metric(telem.system.ram_percent)}%</p>
</section>

<section><h2>LEMONADE</h2>
<p>Status: <strong>{html.escape(lemon_status)}</strong></p>
<p>Target model: {html.escape(LEMONADE_MODEL)}</p>
<p>Active/available: {html.escape(str(lemonade.model_loaded or 'unknown'))}</p>
</section>

<section><h2>HANDOFF</h2>
<p>State: <strong>{html.escape(handoff.state.value)}</strong></p>
<p>VRAM free: {handoff.vram_free_mib or 'n/a'} MiB</p>
</section>

<section><h2>OPTIMIZER</h2>
{opt_html}
</section>

<section><h2>EVENTS</h2><ul>{events_html}</ul></section>

<section><h2>DECISIONS</h2><ul>{decisions_html}</ul></section>

<p style="opacity:0.6;font-size:0.8rem">Governor v0.1 — experimental. Auto-refresh not enabled.</p>
</body></html>"""

    return app


def run_dashboard() -> None:
    import uvicorn

    app = create_app()
    uvicorn.run(app, host=DASHBOARD_HOST, port=DASHBOARD_PORT, log_level="info")
