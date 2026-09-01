# Verified Tests

## Status: Awaiting Evidence

`AMD_Lemonade_Contest_Evidence_Log.md` was not found on this machine at repository creation time. No formal test results, timestamps, or benchmarks are recorded here.

## Tests Implied by Source Code

The following behaviors are implemented in Father Fox and should be verifiable with a live Lemonade + RVC stack, but **have not been captured in this repository**:

| Test | Implementation | Evidence |
|------|----------------|----------|
| Lemonade chat completion | `ask_father_fox()` Model Only path | Source only |
| Lemonade model unload | `release_lemonade_gpu_for_rvc()` | Source only |
| VRAM grace period | `time.sleep(1.0)` after unload | Source only |
| RVC handoff for special voices | `make_voice()` + `SPECIAL_RVC_VOICES` | Source only |
| Auto-reload on next request | Comment in `release_lemonade_gpu_for_rvc()` | Assertion only |
| Whispeer → Lemonade | — | Not found |

## How to Add Tests

1. Run tests against a live local stack
2. Record results in a new markdown file here
3. Sanitize all output before committing
4. Cross-reference entries in `docs/contest-evidence.md`
