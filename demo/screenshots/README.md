# Screenshot Checklist

Place captured images in this directory when ready. **Do not commit fabricated or placeholder images** — this file is the checklist only.

Recommended captures from Trophy Room at **http://127.0.0.1:8771** (see [demo-runbook.md](../demo-runbook.md)):

| # | View | Filename suggestion | What to show |
|---|------|---------------------|--------------|
| 1 | 🏆 Trophy Room main | `01-trophy-room-main.png` | Milestones, Governor panel, +4.22% badge |
| 2 | ⚡ GPU Handoff | `02-gpu-handoff.png` | Timeline (00:17:39–00:20:46), live GPU telemetry |
| 3 | Governor optimization | `03-governor-optimization.png` | THROUGHPUT winner `{480, 0.7}`, candidate decisions |
| 4 | 📜 Evidence Vault | `04-evidence-vault.png` | Expanded Father Fox journal or throughput doc |
| 5 | 🧠 Model Arena | `05-model-arena.png` | `gpt-oss-20b-MXFP4`, verified benchmark constants |
| 6 | 🌐 Local AI Clients | `06-local-ai-clients.png` | Service ONLINE/OFFLINE status grid |

## Capture Tips

- Use 1920×1080 or higher; crop browser chrome if desired
- Ensure no API keys, terminal secrets, or private LAN IPs appear in frame
- Prefer local-only URL (`127.0.0.1:8771`) in address bar for public submission
- Match claims in [verified-results.md](../verified-results.md) — show +4.22%, not pre-fix results

## After Capture

```bash
# Optional: add to git when real screenshots exist
git add demo/screenshots/*.png
```

Until then, this directory contains only this README.
