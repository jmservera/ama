---
title: Issue 188 local handover demo plan
ms.date: 2026-11-01
---

* Research: ../../research/2026-11-01/2026-11-01-issue-188-local-handover-demo-research.md
* Scope: acceptance-criteria demo only; source in `src/api`, tests outside the package; nothing in `mvp/` or `prototype/`.

## Phases

* [x] Phase 1: `src/api/checks/sensor_handover_demo.py` runs the composed local flow and prints the verifier JSON (exit 0 only if `passed` and `idempotent`).
* [x] Phase 2: `src/api/tests/test_sensor_handover_demo.py` runs the demo `main` and asserts pass, idempotence, 24 readings over 2 homes and that a non-zero seam fails.
* [x] Phase 3: README section for the demo command and honest evidence boundary; knowledge-base log entry.
* [x] Phase 4: focused validation (unit tests, ruff check, ruff format --check, mypy); commit, push, PR with `Refs #188`.

## Critique (single pass, executed)

* Verdict: proceed. Findings: the demo must not claim live or Azure proof (applied in output field `evidence` and README); use ephemeral temp store and delete it on exit (applied); no secrets or network (applied).
* Review expectation: one post-implementation review; findings route to follow-ups.

* Correction cycle: reject SQL mode and invalid tolerance in the demo, add tests, rerun checks. Done.
