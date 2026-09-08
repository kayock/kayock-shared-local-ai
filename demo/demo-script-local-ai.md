# Demo Script — Generated Locally by AI

> Generated and revised locally by `gpt-oss-20b-MXFP4` through Lemonade; final factual corrections were checked against the project's verified runtime evidence.

Hi, I’m **gpt‑oss‑20b‑MXFP4**, the local model humming inside your computer, powered by Lemonade. I’m here to show you how we can run a powerful local language model on a modest NVIDIA Quadro P2000 with only 4 GB of VRAM while sharing that GPU with another specialized workload.

---

## The setup

We’re running on a single Quadro P2000. No overclocking, no voltage tweaks, just the stock silicon. Lemonade provides the shared inference runtime and clean unload behavior that lets the application release the GPU when another workload needs it.

## GPU handoff in action

At 00:17:39, Father Fox sends a normal request to Lemonade. At 00:18:08, Father Fox tells Lemonade to unload — the `POST /v1/unload` call. By 00:18:12, Lemonade has released its VRAM for the RVC special-voice workload. The RVC/Father Fox request completes successfully at 00:18:28. The verified return to Lemonade begins at 00:20:15, with the next request completing cleanly at 00:20:46. Both sides of the handoff completed successfully.

## Resource Governor

Behind the scenes, the Resource Governor watches GPU utilization, VRAM usage, temperature, clock speeds, and throttling, plus CPU and RAM. It evaluates bounded software configurations with KEEP, REJECT, or NOT_BEST. The best setup is saved — no overclocking, no disabling thermal protections.

## Performance result

We began with a THROUGHPUT baseline configuration: 512 tokens, temperature 0.7, with a deterministic composite score of **14.639872171624882**. After discovering an optimizer bug, we fixed it, regression-tested the patch, and reran the optimization. The corrected process evaluated a baseline and five candidate configurations. The winning configuration used **max_tokens = 480** and **temperature = 0.7**, with a composite score of **15.25802453529699** — about a **+4.22% improvement in the composite THROUGHPUT score**. That winning run measured a Time-to-First-Token of roughly **6.74 seconds** and generation throughput of about **7.44 tokens per second**.

## Dashboard & evidence

The Trophy Room dashboard shows Lemonade, the model, the GPU, Father Fox, the RVC handoff, the Resource Governor, and the optimization results. Verified runtime and optimization evidence is available in the Evidence Vault for review.

## Looking ahead

Future local apps can reuse the same shared-resource approach, but they are not part of this contest's verified evidence.

---

## In closing

We’ve shown a practical way to make constrained local hardware cooperate across multiple AI workloads — with the evidence committed for review.
