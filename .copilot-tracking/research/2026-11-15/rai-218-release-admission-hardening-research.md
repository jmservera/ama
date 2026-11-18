---
title: "Child Research: Close RV-001 and RV-002 Live Release Admission Hardening (#218)"
description: "Focused three-wave research for child task rai-218-release-admission-hardening resolving RV-001 and RV-002 from parent review"
author: "GitHub Copilot"
ms.date: "2026-11-15"
---

## Research Brief

* Topic: Close `RV-001` (live release dispatch-time and partial-key `OQ-017` admission) and `RV-002` (runtime-binding SQL readiness inspection in `_inspect_sql_live_releases`) for Issue #218
* Task ID / Slug: `issue-218-rai-release-admission-hardening` / `rai-218-release-admission-hardening` (parent: `issue-218-rai-release-discipline` / `rai-218-release-discipline`)
* Purpose: Converge on a minimal, strict-`mypy`-safe core fix and regression test design that closes both routed review defects without breaking existing `src/core` or `src/api` unit suites
* Audience / Use: `rpi-plan`, `rpi-implement`, and `rpi-review` in confirmed automatic RPI Agent child loop
* Output mode: `convergence`
* Resolved evidence root: `.copilot-tracking/research/2026-11-15/`
* Research posture: `focused` (provenance: bounded two-finding core defect follow-up from `.copilot-tracking/reviews/logs/2026-11-15/rai-218-release-discipline-review.md`)
* Explicit limits: Focused validation tier only; do not run `tools/rpi-checks.py`; do not push or open a PR
* Scope: `src/core/src/zava_forward/core/rai_release.py`, `src/core/src/zava_forward/core/assistant_release.py`, `src/core/src/zava_forward/core/rai_control_plane.py`, `src/core/tests/test_rai_control_plane_218.py`, `src/api/tests/test_rai_release_readiness_api_218.py`
* Non-goals: Mutating parent task review artifacts, adding database migrations, or changing HTTP route shapes
* No-interaction rationale: Running in non-interactive automatic mode with exact defect evidence from parent review

## Extension Provenance and Participation

| Extension | Type | Disposition | Provenance & Scoped Contract |
|-----------|------|-------------|------------------------------|
| `.github/copilot-instructions.md` | Instruction (`**`) | Selected | Focused validation tier, strict `mypy`, preserve original review records |
| `rpi-research` | Skill | Selected | Focused three-wave inline investigation (`C#` `path:line` evidence) |
| `RPI Researcher` | Subagent | Skipped (inline) | Tightly coupled 3-file trace across `rai_release.py`, `assistant_release.py`, and `rai_control_plane.py`; investigated inline |

## Cycle 1 Execution

### Wider Wave

Mapped every caller of `rai_release.missing_binding`, `assistant_release.assessment`, `assistant_release.admission`, `assistants.runtime_binding`, and `ai_registry.legacy_binding` across `src/core`, `src/api`, and `src/agents`:

* `C1` (`src/core/src/zava_forward/core/rai_release.py:216-256`): `missing_binding` validates `expires`, `approver`, `serving_model`, `monitoring_declaration`, and `OQ-017` `approved_by` / `named_approval_id`. Currently uses `isinstance(record.get("expires"), (int, float))` without excluding `bool`, and guards `approved_by` and `named_approval_id` individually inside `if live and ("approved_by" in record or "named_approval_id" in record):`.
* `C2` (`src/core/src/zava_forward/core/assistant_release.py:110-137`): `assessment(db, task, binding, now, live=False)` loads persisted SQL rows via `releases(db, task)`, runs `invalidate_changed` for non-legacy tasks, and selects via `rai_release.select(found, spec, binding, BOUND, now, live)`. All live runtime admission paths (`assistants.py:1326`, `assistants.py:1633-1645`, `sqlstore.py:246`) flow through `assistant_release.assessment`.
* `C3` (`src/core/src/zava_forward/core/rai_control_plane.py:948-990`): `_inspect_sql_live_releases` loops over `enabled_tasks` under `with _assistant_release.read_only():`, inspects raw stored fields on `assistant_releases` rows without comparing runtime/legacy bindings or serving-version attestation.

### Deeper Wave

Inspected exact test fixture contracts and binding helpers:

* `C4` (`src/core/tests/test_rai_threshold_live_approval_guard.py:122-132`) and `C5` (`src/core/tests/test_rai_release.py:55-77`): Direct unit tests of `rai_release.missing_binding` and `rai_release.select` pass synthetic 4-key or contract-only dicts that omit both `"approved_by"` and `"named_approval_id"` to test `approver` and `monitoring_declaration` in isolation.
* `C6` (`src/core/tests/release_support.py:11-40`) and `C7` (`src/api/tests/test_assistant_release.py:557-574`): SQL release tests use `release_support.fixture(..., cls="actual")`, which populates `approved_by` and `named_approval_id`. At `src/api/tests/test_assistant_release.py:567-570`, `dict(fx, evidence_class="actual", model_version="test-model")` asserts `assertIn("named-human approved live monitoring thresholds", rel.admission(db, CAP, binding, now, live=True)["missing"])`.
* `C8` (`src/core/src/zava_forward/core/assistants.py:875-895,1630-1646`) and `C9` (`src/core/src/zava_forward/core/ai_registry.py:94-108`): Assistant bindings resolve via `assistants.runtime_binding(task_name, store.ai)`, while legacy bindings resolve via `ai_registry.legacy_binding(task_name, store.ai, ai_registry.legacy_deployment(task_name, store.ai))` under capability key `f"legacy:{task_name}"`.

### Contrarian Wave

Tested two counter-hypotheses:

1. Counter-hypothesis A: Require `"approved_by"` and `"named_approval_id"` unconditionally inside `rai_release.missing_binding(..., live=True)` even when neither key is in `record`.
   * Result (`C4`, `C5`): Rejected for bare `rai_release.missing_binding` because `test_rai_release.py:76` and `test_rai_threshold_live_approval_guard.py:131,201` intentionally pass isolated dicts without `OQ-017` keys and assert `missing == []`. Instead: (a) in `rai_release.missing_binding`, when `"approved_by" in record or "named_approval_id" in record`, require BOTH valid `approved_by` and valid `named_approval_id` (closing partial-key bypass) and reject `isinstance(expires, bool)`; and (b) in `assistant_release.assessment(..., live=True)`, inject `rec.setdefault("approved_by", None)` and `rec.setdefault("named_approval_id", None)` on every SQL-loaded record before `invalidate_changed` and `rai_release.select` so every stored SQL row is unconditionally subject to `OQ-017` at live dispatch time (`C2`, `C7`).
2. Counter-hypothesis B: What if `store.ai` on an offline `Store` has unconfigured/empty `endpoint` or `"unattested"` `model_version` when `_inspect_sql_live_releases` runs `assistant_release.assessment(..., live=True)`?
   * Result (`C1`, `C8`, `C9`): That is the desired fail-closed behavior! When `store.ai` has `"unattested"` `model_version` or a binding mismatch against a stored SQL release row, `assistant_release.assessment(..., live=True)` returns `(None, denial)` because serving-version attestation or bound deployment does not match, keeping `task_name` in `unapproved_live_tasks`. Conversely, when `store.ai` has an attested `model_version` matching a valid `actual` SQL release row (with named `approved_by` and `named_approval_id`), `assessment(..., live=True)` returns `(selected, None)` under `with _assistant_release.read_only():` without mutating SQLite/MSSQL rows.

## Parent Synthesis and Convergence

* Selected recommendation:
  1. In `src/core/src/zava_forward/core/rai_release.py` (`missing_binding`): reject `bool` values on `expires`, and inside `if live and ("approved_by" in record or "named_approval_id" in record):` validate both `approved_by` and `named_approval_id` without inner key-presence guards.
  2. In `src/core/src/zava_forward/core/assistant_release.py` (`assessment`): when `live` is `True`, normalize every loaded SQL record with `rec.setdefault("approved_by", None)` and `rec.setdefault("named_approval_id", None)` prior to `invalidate_changed` and `rai_release.select` so stored/legacy SQL rows cannot bypass `OQ-017` at live dispatch or readiness inspection time.
  3. In `src/core/src/zava_forward/core/rai_control_plane.py` (`_inspect_sql_live_releases`): evaluate each enabled task inside `with _assistant_release.read_only():` via `_assistant_release.assessment(cursor_db, cap, binding, now_ts, live=True)` using `_assistants.runtime_binding` for assistant capabilities and `ai_registry.legacy_binding` for legacy capabilities.
  4. Add focused unit/API regression tests in `src/core/tests/test_rai_control_plane_218.py` and `src/api/tests/test_rai_release_readiness_api_218.py` proving partial-key rejection, stored-SQL-row live dispatch denial without `OQ-017` fields, and drifted-binding SQL readiness rejection.
* Unresolved decisions or blockers: None
* Research disposition: `executed`
* Planning Readiness: `Ready`
