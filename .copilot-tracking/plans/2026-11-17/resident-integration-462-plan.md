---
title: "Plan: resident-integration-462"
description: "Continuation plan for Issue #462: non-rewriting merge of pinned main into the retained candidate plus honest local readiness evidence"
ms.date: 2026-11-17
---

| Field    | Value                                                                  |
|----------|------------------------------------------------------------------------|
| Task     | resident-integration-462 (parent resident-demo-local-gate-462)         |
| Research | [research](../../research/2026-11-17/resident-integration-462-research.md) |
| Details  | [phase details](../../details/2026-11-17/resident-integration-462-phase-details.md) |
| Tier     | FULL (auth, public demo and deployment scope; not downgraded)          |
| Scope    | Local source integration and readiness only. No push, PR, merge to a remote, Azure, secret, model or spend |

## Goal

Make `1c9ac230be1dad9a4ecc21975f9ffe0845309fc4` and `926b20a8856622515c60948bf9ed890b241fc1fc` both ancestors of one frozen local commit, with continuation artifacts, a dated threat-model and knowledge-base update, and recorded light local validation. Preserve every original artifact and adverse result.

## Phases

* [ ] Phase 1: Non-rewriting merge. Require HEAD exactly `926b20a8` first. After `implement-start`, run `git merge --no-commit --no-ff 1c9ac230...`. Resolve only coupled conflicts (none predicted). Never rebase, amend or reset.
* [ ] Phase 2: Dated documentation update in a NEW file `docs/reference/research/resident-demo-threat-model-update-2026-11-17.md` (derived sensor keys `freshness`, `source`, `calibrated`; unchanged 17-column allowlist; validation provenance), a link from the index, an appended log entry and a documentation-only README qualification if the merged README overstates the sensor status line. The 2026-11-16 threat model, research, review and state are not edited (critique PC-001, PC-007).
* [ ] Phase 3: Light local validation from an external venv with this worktree's distributions: resident domain, API, auth, case and projection unit tests; Ruff check and format check; mypy for the resident modules. No `PYTHONPATH=mvp`, no unbounded API suite.
* [ ] Phase 4: Heavy checks. Run any browser process wrapped in `flock -n /tmp/ama-rpi-heavy.lock <command>` so the lock is held for the whole run (PC-002). If held or prerequisites are absent, record the browser, SQL and image checks as named pending continuations. Never queue, sleep or waive.
* [ ] Phase 5: Web review. Fetch current web-interface-guidelines and review the merged `demo.js` change by `file:line`.
* [ ] Phase 6: Witness order (PC-003): `research-open` (done, seq 2), `plan-done` (after this plan, details and critique are persisted), changes artifact persisted, `implement-start`, merge and edits, `implement-done`, one independent review of the final source snapshot (PC-006), `review-done`, one final merge commit, `commit-complete --claim-commit <sha>`. Witness logs stay in the external evidence directory.

## Constraints and decisions

* Preserve fake-email to server-owned synthetic case mapping, positive allowlist and provenance, duplicate and unknown denial, shared-credential and bounded login controls, HTTPS cookie, expiry, logout and CSRF behaviour, no staff or canary fields, unchanged employee Entra login. No write, booking, upload, message, AI or consent path is added. No credential is generated.
* Do not edit `tools/rpi-checks.py`, pins, permissions, Bicep, Dockerfile or application policy. The runner repair on main is taken as merged, not re-derived.
* A skipped or pending check is not a pass. Result vocabulary: FULL RECEIPT / ACTUAL SQL-IMAGE-BROWSER EVIDENCE MISSING, NOT PUBLISHABLE until the coordinator completes the planned checks.
* Eventual PR text uses `Refs #462`; criteria 1, 2, 5, 6 and 7 remain unproved here.

## Success criteria

* `git merge-base --is-ancestor 926b20a8 HEAD` and `git merge-base --is-ancestor 1c9ac230 HEAD` both succeed; the final commit has exactly two parents, first parent `926b20a8` and second parent `1c9ac230` (PC-004), and the tree is clean.
* Original 2026-11-16 files (including the threat model, research, review, state) are byte-identical to `926b20a8` (PC-001).
* Every light check has a recorded command, exit code and skip count; unrun checks are named gaps.
