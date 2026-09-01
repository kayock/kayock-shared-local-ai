# Demo Runbook

Exact steps for recording or live demonstration. **Do not modify production services** during prep — only start Trophy Room.

---

## Prerequisites

- Repository at `/home/kayock/kayock-shared-local-ai` (tag `contest-v0.3-trophy-room` or later on `main`)
- Python 3 with Trophy Room dependencies: `pip install -r trophy-room/requirements.txt`
- Optional: `export LEMONADE_API_KEY="your-local-key"` for Lemonade model list in Trophy Room (never show the key on screen)

---

## Start Trophy Room

### Local-only (recommended for solo recording)

```bash
cd /home/kayock/kayock-shared-local-ai/trophy-room
python app.py
```

Open **http://127.0.0.1:8771**

### Trusted LAN viewing (phones / second device)

```bash
cd /home/kayock/kayock-shared-local-ai/trophy-room
TROPHY_ROOM_HOST=0.0.0.0 python app.py
```

Port: **8771**

**Determine this machine's LAN address** (do not hardcode — it may change):

```bash
hostname -I
```

Use the first address shown, e.g. open `http://<address-from-hostname-I>:8771` from another device on the **same trusted LAN**.

**Warning:** `0.0.0.0` exposes the read-only dashboard to all devices on the local network. No login. Trusted home LAN only.

---

## What Should Be Visible Before Recording

Confirm in Trophy Room before you press record:

| Item | Where to check | Expected |
|------|----------------|----------|
| Lemonade | Local AI Clients / status | **ONLINE** (if Lemonade is running) |
| Father Fox | Local AI Clients | **ONLINE** (if service active) |
| Governor | Local AI Clients | **ONLINE** (if dashboard running on :8770) |
| RVC | Local AI Clients | **ONLINE** (if Kayock Voice running) |
| GPU telemetry | GPU Handoff / header | Live VRAM, utilization (if NVIDIA GPU present) |
| Model | Model Arena | **gpt-oss-20b-MXFP4** |
| Optimization | Trophy Room / Governor panel | **+4.22%** verified THROUGHPUT |
| Handoff timeline | GPU Handoff | Timestamps 00:17:39 … 00:20:46 |
| Evidence | Evidence Vault | Sanitized journal + optimization docs |

**Offline services are OK for demo** — Trophy Room shows PLANNED/OFFLINE honestly. For the strongest live demo, start Father Fox, Lemonade, Governor, and RVC before recording.

---

## Recording Flow

Follow [demo-script.md](demo-script.md). Suggested tab order:

1. 🏆 Trophy Room (milestones + Governor panel)
2. ⚡ GPU Handoff (timeline + live GPU)
3. 🧠 Model Arena (model + benchmark constants)
4. 📜 Evidence Vault (expand journal excerpt)
5. 🌐 Local AI Clients (service status)

---

## Pre-Demo Checklist

- [ ] On branch `main` at or after `contest-v0.3-trophy-room`
- [ ] Trophy Room dependencies installed
- [ ] Trophy Room starts without errors on port **8771**
- [ ] Browser opens http://127.0.0.1:8771 (or LAN URL from `hostname -I`)
- [ ] No API keys visible in terminal, browser, or screen share
- [ ] Production services running if you want live ONLINE badges (optional)
- [ ] Screen resolution readable (1080p minimum recommended)
- [ ] Notifications silenced
- [ ] [demo-script.md](demo-script.md) reviewed

---

## Post-Demo Checklist

- [ ] Stop Trophy Room test server (`Ctrl+C`) if you started it manually
- [ ] Capture screenshots per [screenshots/README.md](screenshots/README.md) (optional)
- [ ] Verify recording shows verified timestamps and +4.22% (not pre-fix buggy result)
- [ ] No private LAN IP addresses left in exported video metadata overlays you added
- [ ] Copy submission text from [contest-summary.md](contest-summary.md) if submitting
- [ ] Link judges to [verified-results.md](verified-results.md) and [demo/README.md](README.md)

---

## Ports Reference

| Service | Port |
|---------|------|
| Father Fox | 8765 |
| RVC | 8766 |
| Governor dashboard | 8770 |
| **Trophy Room** | **8771** |
| Lemonade | 13305 |

---

## Troubleshooting

| Issue | Action |
|-------|--------|
| Trophy Room won't start | Check port 8771 free: `ss -tlnp \| grep 8771` |
| All services OFFLINE | Expected if production not running; use Evidence Vault for verified claims |
| Lemonade models empty | Set `LEMONADE_API_KEY` in shell before `python app.py` (do not display key) |
| LAN device can't connect | Confirm same Wi-Fi, firewall allows 8771, use `hostname -I` address |
