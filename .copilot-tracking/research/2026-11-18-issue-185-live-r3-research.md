---
title: Research for issue 185 live device identity demo (run 3)
date: 2026-11-18
---

Research disposition: executed (reuses the earlier note and run-2 log).

Gaps left by runs 1 and 2: operator-side results (show-stats, job and role removal) had no retained raw output; the home-to-identity mapping was only source-tested. Run 3 retains the raw operator output (redacted of identifiers) and binds each device id to a stock home id using the repository `sensor_identity`/generator code inside the job.

Owner scope: Hub-generated symmetric keys, no X.509, no Key Vault rotation, demo only. Hub `[hub]` has public access Disabled, so a throwaway Container Apps job is needed. Existing state JSON `issue-185-live-state.json` is not overwritten; this run uses `issue-185-live-r3-state.json`.

Planning Readiness: Ready.
