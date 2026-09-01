# Demo Script — Generated Locally by AI

> Generated and revised locally by `gpt-oss-20b-MXFP4` through Lemonade; final factual corrections were checked against the project's verified runtime evidence.

Hi, I’m **gpt‑oss‑20b‑MXFP4**, the local model humming inside your computer, powered by Lemonade. I’m here to show you how we can squeeze a powerful language model into a modest NVIDIA Quadro P2000 that only has 4 GB of VRAM.

---

## The setup

We’re running on a single Quadro P2000. No overclocking, no voltage tweaks, just the stock silicon. Lemonade provides the shared inference runtime and clean unload behavior that lets the application release the GPU when another workload needs it.

## GPU handoff in action

At 00:17:39, Father Fox sends a normal request to Lemonade. The model loads, processes, and returns a response. At 00:18:08, Father Fox tells Lemonade to unload – the POST /v1/unload call. Lemonade frees the VRAM, and by 00:18:12 the RVC special‑voice workload grabs the GPU. The RVC/Father Fox request completes successfully at 00:18:28. The verified return to Lemonade begins at 00:20:15, with the next request completing cleanly at 00:20:46. Both sides of the handoff completed successfully.

## Resource Governor

Behind the scenes, the Resource Governor watches GPU utilisation, VRAM usage, temperature, clock speeds, and throttling, plus CPU and RAM. It evaluates every configuration with KEEP, REJECT, or NOT_BEST. The best setup is saved – no overclocking, no disabling thermal protections. Just the right balance for this limited hardware.

## Performance win

We began with a baseline configuration: 512 tokens, temperature 0.7, scoring **14.639872171624882**. After discovering an optimizer bug, we fixed it, regression‑tested the patch, and reran the optimisation. The corrected process evaluated a baseline and five candidate configurations. The winning configuration used **max_tokens = 480** and **temperature = 0.7**, scoring **15.25802453529699** – an improvement of about **+4.22 %**. That winning setup achieved a Time‑to‑First‑Token of roughly **6.74 seconds** and a throughput of about **7.44 tokens per second**. A small tweak, a noticeable bump, all on the same 4 GB card.

## Dashboard & evidence

The trophy‑room dashboard shows Lemonade, the model, the GPU, Father Fox, the RVC handoff, the Resource Governor, and the optimisation results. Verified runtime and optimization evidence is available in the Evidence Vault for review.

## Looking ahead

We’re building a private family local‑AI LAN, so future apps like NOMAD, Comic Reader, or Audio Notebook can share the same GPU. But for now, we’re focused on making the model and the hardware cooperate, not on buying a bigger GPU.

---

## In closing

We’ve proven that local AI can thrive with the hardware you already have – turning a 4 GB card into a collaborative, high‑performance partner.
