---
title: Plan for issue 185 live device identity demo (run 3)
date: 2026-11-18
---

1. [x] Create throwaway job `job-185c-probe` (demo API image, `id-cutover-test-api`) and a temporary Registry Contributor assignment.
2. [x] Driver maps three stock homes to `SYN-<sensor_key>` ids with repository `sensor_identity`, creates Hub-key devices, sends with each key, wrong-key contrast, deletes, reads back, leak-checks.
3. [x] Retain raw job output and raw operator output (show-stats, job list, role list), redacted.
4. [x] Delete job and role; document per-criterion result. No source edits; focused tier.
