<!-- markdownlint-disable-file -->
# Research: gate benchmark for #470 (2026-11-02)

* Task: `gate-benchmark-470`. Research disposition: executed (small, local).
* Planning Readiness: Ready.

## Findings

* Only open criterion of #470: "Measured full-run time before and after is recorded in the PR". The issue's 23 to 26 minute figure is session evidence from 17 runs, not a controlled measurement.
* "Before" = original serial path: `--all --jobs 1` (default). "After" = `--all --jobs N`. `worker_limit` in `tools/rpi-checks.py` caps workers at `min(N, cpus // 2, (MemAvailable - 1 GiB) // 4 GiB)`. On 4 vCPU / 15 GiB the cap is 2, so `--jobs 3` (as in src/README.md) runs 2 workers; the benchmark uses `--jobs 2` and records the effective value.
* The heavy lock `/tmp/ama-rpi-heavy.lock` is contended: other agents run queued gates (`/tmp/gatequeue*`). An idle measurement therefore needs the benchmark to hold the lock for both runs. The tool supports `--heavy-lock-fd` for that, so no other gate can start between the two runs.
* Per-command start and end times are in each receipt (`commands` rows), which allow per-group wall time. Groups running in parallel overlap, so per-group wall times do not sum to the total.
* Docs target: the "Local RPI gate" section of `src/README.md`.

## Caveats to record

* Single run per arm; no repetition, so no variance estimate.
* Cache state differs between arms (pip/Docker/Trivy caches) unless both start from the same state; record what was observed.
* Other host activity (agent processes) is not controlled; load average is recorded.
