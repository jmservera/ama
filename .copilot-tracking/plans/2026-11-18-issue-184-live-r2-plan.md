# Plan: issue 184 live simulator stream, run 2

1. [x] Create throwaway devices `SYN-<sensor>` for homes ZF-2025-0029 to 0031 with Hub-generated SAS keys; temp roles; job `job-184r2-probe`.
2. [x] Run repository `live_simulator.run` (cadence 1 min, 3 slots) with an out-of-repo SAS sink over the hub.
3. [x] Read Event Hub `sensor-readings` from run start; compare device id, message id and body with what was sent.
4. [x] Delete devices, job, role assignments; verify with `az`.
5. [x] Retain redacted raw job output in `docs/reference/research/`; write evidence note with per-criterion table; re-read children state.
6. [x] Review, commit (no push).

Tier: FOCUSED, no src change. Keys in memory only; output carries ids and codes only.
