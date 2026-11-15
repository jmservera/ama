---
title: Cross-epic stabilization journey research (#440)
ms.date: 2026-11-14
task_id: 440-cross-epic-stabilization-0247
---

## Scope

Local-first regression and integration check for stabilization criterion #440 across In Progress Epics #165 (synthetic data), #104 (bounded AI) and #149 (accessible workbench). Refs #104, Refs #149, Refs #165, Refs #440. Research disposition: executed. Planning Readiness: Ready.

## Evidence

* `src/api/pyproject.toml`: `mypy` is strict over `src`, `tests`, `checks`; `zava_forward.core.*` and `server` are skipped, so `App(...)` is an untyped call that needs a targeted ignore. The file is not modified.
* `src/core/src/zava_forward/core/synthetic/privacy.py`: `record_issues`, `emission_issues`, `pattern_issues(scale_home=True)` give typed label and pattern checks. `provenance.py`: `file_hashes`, `source_revision`.
* Fixture `tests.test_mvp.DATA` carries invented phone numbers and TE1 1ST postcodes, so only name, formal name, email and home fields are pattern-scanned; map anchors are lat 0, lon 0.
* `POST /api/ai/priority` with no provider returns `source=template`, `model=null`, `status=Proposed`, `fallback_reason` set, deterministic list and per-item `cites`. `mode=ai` and `mode=workflow-only` both fail closed to the template.
* `POST /api/chat/threads` returns 403 until DPIA, lawful basis and notice references exist; `GET /api/chat/status` reports storage not approved, activation disabled, one call per turn, no retries, no memory.
* Web cues: `index.html` skip link and polite status region, `style.css` glyph pseudo-content for danger, ok and wait, reduced-motion media query, "Workflow-only" labels in `case-workspace.js` and `chat.js`, manual-path copy in `app.js`.

## Unknowns and limits

* Local evidence only: no hosted CI, browser or accessibility conformance claim.
* `/api/cases` lists a permitted subset, so the journey asserts a subset of loaded cases.
