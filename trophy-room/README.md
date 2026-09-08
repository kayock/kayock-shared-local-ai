# Kayock Local AI Trophy Room

**Contest showcase and observability dashboard** — not an AI runtime.

## Purpose

Visually demonstrate Kayock Shared Local AI within seconds:

- Verified milestones (Father Fox, Lemonade, RVC handoff, Governor)
- Live read-only GPU telemetry
- GPU handoff lifecycle with runtime evidence timestamps
- Governor THROUGHPUT optimization (**+4.22% composite score**, verified)
- Sanitized evidence vault

## Architecture

```
Browser → Trophy Room (FastAPI :8771)
              ├── adapters/telemetry.py  → Governor nvidia-smi collector
              ├── adapters/services.py   → HTTP health probes (read-only)
              ├── adapters/evidence.py   → Repository markdown evidence
              └── adapters/governor_data.py → Verified constants + SQLite (ro)
```

Trophy Room does **not** call `/v1/unload`, modify Lemonade, or control Father Fox.

## Run

### Local-only (default)

Binds to **127.0.0.1:8771** — only accessible from this machine.

```bash
cd /home/kayock/kayock-shared-local-ai
pip install -r trophy-room/requirements.txt
# Optional for Lemonade model list:
export LEMONADE_API_KEY="your-local-key"

cd trophy-room
python app.py
```

Open **http://127.0.0.1:8771**

### LAN demo (trusted network only)

To show the dashboard on phones or other devices on your local network:

```bash
TROPHY_ROOM_HOST=0.0.0.0 python app.py
```

Optional custom port:

```bash
TROPHY_ROOM_HOST=0.0.0.0 TROPHY_ROOM_PORT=8771 python app.py
```

Then open `http://<this-machine-hostname-or-ip>:8771` from another device on the same LAN.

**Warning:** LAN mode (`0.0.0.0`) exposes the read-only dashboard to every device on your local network. There is no login. Use only on a **trusted home LAN**. Default `127.0.0.1` is recommended for everyday use.

| Variable | Default | Purpose |
|----------|---------|---------|
| `TROPHY_ROOM_HOST` | `127.0.0.1` | Bind address (`0.0.0.0` for all interfaces) |
| `TROPHY_ROOM_PORT` | `8771` | HTTP port |

Port **8771** does not conflict with Father Fox (8765), RVC (8766), Governor (8770), or Lemonade (13305).

## Views

| Tab | Content |
|-----|---------|
| 🏆 Trophy Room | Milestones + Governor panel |
| 🧠 Model Arena | Model info + verified benchmarks |
| ⚡ GPU Handoff | Lifecycle diagram + live GPU |
| 🌐 Local AI Clients | Detected/planned services |
| 📜 Evidence Vault | Expandable sanitized evidence |

## Data Sources

| Source | Type |
|--------|------|
| Repository markdown evidence | Static (committed) |
| `governor/data/governor.sqlite` | Live read-only (optional) |
| nvidia-smi / psutil | Live polling (4s) |
| Service health URLs | Live polling |

## Detected Local Systems (2026-09-01)

| System | Status |
|--------|--------|
| Father Fox | **ONLINE** — verified |
| Lemonade | **ONLINE** — verified |
| Governor dashboard | **ONLINE** on :8770 |
| Kayock Voice RVC | **ONLINE** on :8766 |
| Whispeer | **PLANNED** — no source |
| NOMAD | **PLANNED** |
| Comic Reader | **PLANNED** — not part of this contest evidence |
| Audio Notebook | **PLANNED** — not part of this contest evidence |

## Security

- API keys read from environment server-side only
- Never embedded in HTML or JavaScript
- Evidence sanitized (no private IPs, no keys)
- Does not read `/etc/father-fox-lemonade.env`
- Binds to `127.0.0.1` by default; set `TROPHY_ROOM_HOST=0.0.0.0` only on a trusted LAN

## Tests

```bash
cd /home/kayock/kayock-shared-local-ai
pip install pytest httpx
PYTHONPATH=trophy-room:. pytest trophy-room/tests/ -v
```

## Verified vs Planned

- **VERIFIED** — backed by committed runtime evidence
- **VERIFIED EXPERIMENTAL** — Governor v0.1 with live optimization evidence
- **PLANNED** — not demonstrated in this contest repository

The Governor's reported **+4.22%** is the improvement in its deterministic composite THROUGHPUT score from the corrected live optimizer run. Raw TPS and TTFT are reported separately.
