---
title: Issue 1360 extension E1 critique (one pass, self-run, not independent)
ms.date: 2026-11-10
task_id: 1360-extension1-1110
---

## Execution and verdict

Critique executed once on the final candidate plan and details, by the same session (no nested agents). Verdict: approve with direct applications. This is not an independent review and does not replace Root's exact-head assessment.

## Findings and dispositions

1. The core tuple widening changes a shared path (all `SqlStore.save` callers), which sits near the owner rule against a broad exception refactor. Disposition: kept, because only the single post-commit reload is widened, nothing before `COMMIT` changes, and the class already exists for exactly this outcome. Recorded as the main residual risk for Root.
2. `ValueError` and `OSError` from the post-commit reload could hide a corrupt-row problem behind a "saved, refresh did not settle" message. Disposition applied: chain with `from error` so the cause stays inspectable, assert `__cause__` in the core test, and keep `_seq = -1` so the next read reloads.
3. A wording-only CLI change was rejected: it cannot separate pre- and post-commit, and would weaken a true message. No CLI hunk. Confirmed against the original adverse diagnostic, which suggested wording only as a conservative alternative.
4. The regression must inject only after the commit, using a read-only connection as proof, not a mocked `save`. Applied in details.
5. `sqlite3.Error` from the same reload keeps its existing "not known whether" arm; not widened. Applied.
6. Sibling scopes 1419, 132, 131 and 80 touch no owned hunk. Overlap risk is the shared `sqlstore.py`; report only.
7. The MSSQL store has no tested post-commit path here. Disposition: unobserved, stated as a limit in the handoff.

No finding conflicts with a confirmed owner decision, and no user decision is required. No second critique will run.
