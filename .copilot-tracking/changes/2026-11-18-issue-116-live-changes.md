---
title: Issue 116 live demo changes
ms.date: 2026-11-18
---

## Changes

Docs and evidence only; no src change. Note: the witness `implement-start` was refused once (state had no changes path), then accepted with the qualification that the docs and evidence already existed (live probing preceded the changes file).

* Added `docs/reference/research/issue-116-live-demo-evidence-2026-11-18.md`.
* Index entry in `docs/reference/README.md`; entry appended to `docs/reference/log.md`.
* Evidence under `.copilot-tracking/evidence/2026-11-18/issue-116-live/`.

## Validation

* Tier: FOCUSED (documentation and evidence only; no source, workflow, dependency, SQL or infrastructure change). Basis: `git diff` lists only docs and tracking files.
* `src/core`: `unittest test_ai_provider_payload_spy test_data_protection test_ai_input_bounds` 52 OK.
* `src/api`: `unittest test_document_controls test_assistants` 157 OK, 60 skipped.
* Mypy, ruff and `rpi-checks.py` not applicable (no Python package change); `--all` deliberately not run.
* Secret scan of evidence for the employee account name and password: no match.
* Hosted CI not observed (nothing pushed).

## Per-criterion result

| # | Criterion | Status |
| --- | --- | --- |
| 1 | Roles allowed to see a vulnerability reason confirmed (OD-14, OD-19) | Unproven: enforcement observed for one reason role; confirmation is a human decision excluded for the demo |
| 2 | Allowlists at every provider boundary | Unproven live: only the unknown-task refusal observed; offline spies cover implemented paths |
| 3 | Permissions rechecked on outputs, citations, errors, review records, exports | Unproven: one role read, no stored output or second role to compare |
| 4 | Document AI needs approved derivative or necessity exception | Unproven live: no uploaded document in the demo; offline hold tests pass |

All four boxes stay unticked.
