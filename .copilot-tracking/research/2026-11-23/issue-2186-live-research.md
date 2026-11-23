# Issue 2186 research: inert paths for full receipts (2026-11-23)

Disposition: executed. Planning Readiness: Ready.

## Evidence

* `tools/rpi-checks.py` `inert_path` treats any `.md` and `docs/`, `.copilot-tracking/`, `support/` as inert. `changed_groups`, `moved_path_blocker` and `base_relaxation` (full receipt, `inert_only`) all use it.
* Tests read root `README.md` (`tools/test_production_claim_guard.py`), `infra/README.md` (`infra/tests/test_governance.py`) and `docs/**` (`src/core/tests/test_live_doc_links.py` globs every `*.md` except `.git`, `.copilot-tracking`, `node_modules`, `.venv`, `support`; `test_governance.py`, `test_usability_programme.py`, `test_chat_dpia_record.py` read named docs).
* Only `.copilot-tracking/` and `support/` are provably unread (explicitly skipped by the link test).
* `moved_path_blocker` returns early on inert paths, so a path changed by both main and the candidate skips the "also changed by the candidate" check.

## Decision

* Add `receipt_inert_path`: only `.copilot-tracking/` and `support/`; use it for full-receipt relaxation. `changed_groups` keeps `inert_path` (selection semantics unchanged).
* Check candidate-changed before the inert shortcut.
* Tier: tooling only (no `src/` change), focused tier; `--all` not run.

## Acceptance criteria (issue 2186)

Evidence for each is in the changes record per-criterion table. The live Azure and browser aspects do not apply: the issue concerns a local gate tool.
