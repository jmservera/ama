# Research: sensor checkpoint qualification (2026-11-10, Refs #440 #109 #111)

Disposition: executed. Planning Readiness: Ready. Docs only; no source, test, runtime, gate, cloud, model or counter work.

## Findings

* Original candidate `80643f6b9cafa4e33ccd7afab77cbc7c282ab496` (tree `7652c679926f`, base `4c1b4099`) and its seven events (`phase440-sensor-actual-main-evidence-1110`) stay intact. Its witness `verify` exited 1 (QUALIFIED: review artifact changed after observation at seq 6, because two review lines were edited after `review-done`). That adverse result is preserved, not healed.
* PR 1405 (aftercare checkpoint, head `5450b07a89a6`) merged 2026-11-10T16:44:27Z as `ac962fe6ce0faf89539e13606d2a0f1498a59f7a` (tree `a1ac49c7`). The original sensor section says PR 1405 was OPEN and not on main; that was true of the `4c1b4099` snapshot and is now historical.
* Fresh `origin/main` read after 16:50Z is `8eb87b443e2eec107859d74ba754214fff43c58c` (PR 1407, tree `2965af27b37b`). A concurrent fetch race showed main can still move, so the final base is re-resolved at implement time and stated exactly.
* Source: `src` `49c7b0b06f97`, `infra` `f7f31c0934cf`, `tools` `432a4e8f7d74` and `.github` `ce96a8f4c2c5` on that main equal those on `4c1b4099`; paths changed since `4c1b4099` outside `.copilot-tracking` are only `docs/architecture/cutover-evidence-pack.md`, `docs/reference/README.md` and `docs/reference/log.md`. Runtime source therefore remains the sensor `4c1b4099` source.
* A trial merge-tree of this branch with main conflicts in the pack, index and log (both sides appended at the same end). Resolution must keep both append-only sections.
* Execution qualification unchanged: raw runs were on staged `d45426bd` (equal `src`/`infra`/`tools`/`.github` to `6fe2218c`); main differs only by `.github/rubric/scores/latest.json`; no fresh main runtime claim.

## Planning Readiness

Ready.
