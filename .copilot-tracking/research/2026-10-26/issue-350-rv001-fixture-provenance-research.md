<!-- markdownlint-disable-file -->
---
title: Issue 350 RV-001 fixture provenance research
description: Prospective research into replacing hand-assembled contact and AI checker fixtures with runtime-produced synthetic evidence
ms.date: 2026-10-26
---

Written 2026-10-26 from about 07:20Z, before the plan, details, critique and any source edit. Starting point: clean local head `a1c32b6a6c3c8b41ad30e0e3f49666542872a25c`; nothing pushed. This is new prospective work for the residual RV-001 gap and is not retroactive compliance for earlier process gaps. Earlier reviews are unchanged.

The gap (RV-001, Medium, from the coordinator's whole-content assessment): `tools/test_check_demo_feedback.py` builds the contact lists (`contact`, `case_write`), the audit ledger reports (`ledger_report`) and the AI record (`ai_record`) by hand. The checker can pass them while the real runtime would emit a different shape, so fixture-to-runtime drift is not detected. `staff_me` already calls `projection.me_payload`, `navigation`, `taskqueues.contract` and `ranking.CURRENT`, so the `me` path is runtime-derived. `ledger_report` already uses `ledger.make_entry` and `verify_entries`.

Runtime producers found (installed source, call path used by `src/api/src/zava_forward/api/server.py`):

* Write: `POST /api/cases/{id}/call` calls `Store.log_call(user, case_id, outcome, note, channel)` (`store.py` ~480). It truncates the outcome to 80 characters, the note to 500, appends the contact `{at, purpose, channel, direction, outcome, note, by}`, and audits `log_contact`.
* Read (before, write response and reload): `GET /api/cases/{id}` calls `Store.detail(case_id, user)`; contacts are returned newest first, capped at 40 (`store.py` 402).
* Audit report: `GET /api/audit-check` returns `Store.verify_ledger()`.
* AI: `POST /api/ai/priority` returns `Store.ai_priority(user, n, mode)` (`store.py` ~783), built from `_rec_view` with label `Store.REC_LABEL`, items from the model text via `ai_tasks.priority_items`, release from `ai.run`.
* The AI boundary is `Ai._chat`; existing runtime tests (`src/api/tests/test_ai_tasks.py`) replace `store.ai._chat` with a scripted callable and set `store.ai.endpoint` to a `.invalid` host. Release admission uses `release_support.install(store)` from `src/core/tests/release_support.py`; for a JSON `Store` it installs an explicit offline output-test release (`offline-output-test:priority`, version `scripted-output-v1`), never a production option.
* Constructed data: `src/core/tests/dataset.py` `DATA` (five cases, two staff), used by existing store tests with `Store(path, live_path, audit_path)`.
* Restart: constructing a second `Store` over the same `live.json` and `audit.jsonl` reloads persisted state (`make_again` pattern in existing tests). This is a JSON-store reload, not SQL durability.

Chosen simplest route: build a JSON `Store` from `dataset.DATA` in a temporary directory, script `_chat` (the external AI boundary), install the offline test release, then call the same `Store` methods the server calls to produce `before`, `write`, `after` (from a second Store over the same files), `audit_before` and `audit_after`, and the bare `ai_priority` record. No runtime logic is copied, and no real model, network, Azure, SQL or secret is used.

Constraints and risks recorded now:

* `dataset` and `release_support` live under `src/core/tests` and are not installed distributions. The tools test must locate them from the repository layout (path of the test file) and, if unavailable, report a visible skip with the reason rather than silently weaken coverage. The editable venv resolves `zava_forward` to this worktree.
* `tools/test_check_demo_feedback.py` is not in the `tools/rpi-checks.py` gate list; this is existing behaviour and is not changed here.
* The runtime AI record carries extra fields (`deterministic`, `final_items`, `actionable` and others); the checker reads only the fields it names, so no checker change is expected. A real mismatch discovered while running would be reported as a material choice, not fixed silently.
* The runtime `rank` and `resident` values come from the case data. The release in the record is an offline output-test release and must not be described as real release admission. The checker already says model and release are self-reported by the capture, and it keeps `spend_bound` and `admin_account` not-run so overall never passes.
* Constructed fixture, the 980-total seed, 443 open and the checker default 980 open-programme baseline stay distinct. No live count is captured and no default changes.

Residual limits unchanged: this does not exercise real inference, real release admission, SQL durability, a deployed server or acceptance; heavy gate #360 holds the single gate; no `--lock-timeout 14400`; when a gate is later run it must use the coordinator's non-blocking `--lock-timeout 0`. Disk is 6.8 GB free.
