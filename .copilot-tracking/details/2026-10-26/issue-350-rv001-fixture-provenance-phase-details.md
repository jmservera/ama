<!-- markdownlint-disable-file -->
---
title: Issue 350 RV-001 fixture provenance phase details
description: Prospective phase details
ms.date: 2026-10-26
---

* Phase 1: one read-only `rubber-duck`; critique file `reviews/plans/2026-10-26/issue-350-rv001-fixture-provenance-critique.md`; commit research, plan, details and critique before any source edit.
* Phase 2: the builder locates `src/core/tests` from `Path(__file__).resolve().parents[1] / "src" / "core" / "tests"` and appends it to `sys.path`; it imports `dataset` and `release_support`. It copies nothing from them. The Store is built in `tempfile.TemporaryDirectory` with `Store(data, live, audit)`. `store.ai.endpoint` is set to a `.invalid` host and `store.ai._chat` to a scripted callable returning a JSON list of cited priority items for an owned open case; `release_support.install(store)` supplies the offline release. Staff user is `DATA["staff"][0]`. Evidence assembly: `before = detail(case)`, `log_call`, `write = detail(case)`, second Store, `after = detail(case)`, `audit_before` and `audit_after` from `verify_ledger()` taken around the write, `ai = ai_priority(user, 1)` JSON round-tripped. Request echoes the submitted outcome, note and channel. Responses are wrapped as `{status: 200, body: ...}` and round-tripped through `json` as the live capture would be.
* Failing first: the tests reference the builder before it exists, so they fail with an import or attribute error; then the builder is added and the tests pass.
* Negative tests mutate a deep copy of the runtime-produced evidence: drop the new contact, change the outcome, set `source` to `template`, empty `cites`, break the audit chain. Each must produce `fail` (or `blocked` where the checker's existing contract says so).
* Phase 4 command from the repo root: `PYTHONDONTWRITEBYTECODE=1 /home/azureuser/rehearsal-350/venv/bin/python -m unittest tools.test_check_demo_feedback`; confirm the editable binding by printing `zava_forward.core.__path__` first. Remove any `__pycache__` afterwards.
* Phase 5: read-only `rubber-duck` over `git diff` of tools, its own run of the tests, and the disposition text.
* Phase 6: write review, changes, state; commit; gate readiness report. The later gate, if released, uses `--lock-timeout 0` as the coordinator now requires.
