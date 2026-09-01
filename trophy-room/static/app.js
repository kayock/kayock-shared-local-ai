const POLL_MS = window.POLL_INTERVAL_MS || 4000;

function badgeClass(badge) {
  if (!badge) return "badge-planned";
  if (badge.includes("EXPERIMENTAL")) return "badge-experimental";
  if (badge === "VERIFIED") return "badge-verified";
  return "badge-planned";
}

function setChip(id, value, online) {
  const el = document.getElementById(id);
  if (!el) return;
  el.textContent = value;
  el.classList.remove("online", "offline");
  if (online === true) el.classList.add("online");
  if (online === false) el.classList.add("offline");
}

async function pollStatus() {
  try {
    const resp = await fetch("/api/status");
    const data = await resp.json();

    setChip("live-lemonade", data.lemonade.online ? "ONLINE" : "OFFLINE", data.lemonade.online);
    setChip("live-father-fox", data.father_fox.status === "online" ? "ONLINE" : "OFFLINE",
      data.father_fox.status === "online");
    setChip("live-governor", data.governor.status === "online" ? "ONLINE" : "OFFLINE",
      data.governor.status === "online");

    const gpu = data.gpu || {};
    setChip("live-gpu-util", gpu.utilization_percent + "%");
    setChip("live-vram", gpu.vram_used_mib + " / free " + gpu.vram_free_mib + " MiB");
    setChip("live-temp", gpu.temperature_c + " °C");

    const liveGpu = document.getElementById("live-gpu-panel");
    if (liveGpu) {
      liveGpu.innerHTML = `
        <div class="metrics-grid">
          <div class="metric"><div class="val">${gpu.utilization_percent}</div><div class="lbl">GPU %</div></div>
          <div class="metric"><div class="val">${gpu.vram_used_mib}</div><div class="lbl">VRAM used MiB</div></div>
          <div class="metric"><div class="val">${gpu.vram_free_mib}</div><div class="lbl">VRAM free MiB</div></div>
          <div class="metric"><div class="val">${gpu.temperature_c}</div><div class="lbl">Temp °C</div></div>
          <div class="metric"><div class="val">${gpu.clock_mhz}</div><div class="lbl">Clock MHz</div></div>
          <div class="metric"><div class="val">${gpu.throttle}</div><div class="lbl">Throttle</div></div>
        </div>`;
    }
  } catch (e) {
    console.warn("poll failed", e);
  }
}

document.querySelectorAll(".tab").forEach((tab) => {
  tab.addEventListener("click", () => {
    document.querySelectorAll(".tab").forEach((t) => t.classList.remove("active"));
    document.querySelectorAll(".panel").forEach((p) => p.classList.remove("active"));
    tab.classList.add("active");
    const panel = document.getElementById(tab.dataset.panel);
    if (panel) panel.classList.add("active");
  });
});

pollStatus();
setInterval(pollStatus, POLL_MS);
