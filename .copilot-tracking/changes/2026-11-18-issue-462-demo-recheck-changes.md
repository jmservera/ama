---
title: Changes record for #462 synthetic showcase demo recheck
ms.date: 2026-11-18
---

* Status: complete. Tier FOCUSED (documentation and evidence only; no `src/`, infra or Azure change; no throwaway resource created, so nothing to delete).
* Added: [recheck note](../../docs/reference/research/resident-showcase-live-recheck-2026-11-18.md); evidence folder `.copilot-tracking/evidence/2026-11-18-resident-showcase-recheck/` (scripts, JSON, five screenshots); research, plan, details, critique, changes and review artifacts for this task.
* Edited: `docs/reference/README.md` (index row), `docs/reference/log.md` (entry), state file.
* Validation: live Playwright run (36 checks) and override diagnosis, exits 0; Azure read-only queries; link and diff review. Unit tests, mypy and ruff not applicable (no code in `src/` or `infra/` changed). Hosted CI not observed.
* Operational note: repeated failed logins from one source trip the 5 per 600 seconds limiter, which delayed the diagnosis run by about 25 minutes; no cookie or credential was printed.

## Per-criterion table

| Criterion | Result |
|-----------|--------|
| 1. Prospective RPI artifacts and threat model | Proven (this run and earlier runs; original October independent review not re-derived) |
| 2. #444/#455 and failed rubric resolved | Unproven: needs a hosted run on a pushed head |
| 3. (ticked) Login, denials, canaries | Re-observed live |
| 4. (ticked) Secret and session controls | Re-observed live |
| 5. (ticked) Local gates | Not re-run, no source change |
| 6. Pre-spend record, cap, stop plan | Proven for the demo; USD 440.90 actual since 2026-10-01, USD 89.15 month to date, about USD 259 left of USD 700; forward forecast not produced |
| 7. Real HTTPS browser verification | Proven for the demo, desktop only |
| 8. (ticked) Image, URL, resources, expiry | Refreshed; source commit behind digest unconfirmed |
