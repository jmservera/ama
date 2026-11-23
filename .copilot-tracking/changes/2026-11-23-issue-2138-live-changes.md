---
title: Issue 2138 live changes
---

Files: research note and evidence folder under docs/reference/research/, README index entry, log entry. No src change. Azure: one throwaway job `job-demo2138-probe` created and deleted; job list verified back to five.

Targeted tests: core 110 OK, orchestrator 11 OK, API 49 OK.

| Criterion | Status |
| --- | --- |
| Named policy owner signs the first rule order | Unproven, owner-gated (live policy unsigned, owner `to be named`) |
| Ranking snapshot publication is scheduled and retained (ADR 0002 deviation) | Partly proven on main and in 2026-11-18 throwaway run; unproven live (no job deployed, image lacks module, unsigned policy, no approved retention) |
