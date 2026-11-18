<!-- markdownlint-disable-file -->
# RPI Phase Details: Surface Retained Sensor Values and Ground Quality AI Review Flags (Issue #1288)

## Metadata

* Task ID: quality-1288-sensor-ai-2142
* Task slug: quality-1288-sensor-ai-2142
* Related plan: .copilot-tracking/plans/2026-11-14/quality-1288-sensor-ai-2142-plan.md
* Evidence sources: .copilot-tracking/research/2026-11-14/quality-1288-sensor-ai-2142-research.md, GitHub Issue #1288, .github/copilot-instructions.md

## Phase Index

| Phase ID | Name                                                               | Status    | Detail sections          |
|----------|--------------------------------------------------------------------|-----------|--------------------------|
| P01      | Core Retained Sensor Conflict Propagation and Provenance Grounding | completed | P01, P01-T01, P01-T02    |
| P02      | Quality AI Review Flag Source Provenance and Conflict Gating       | completed | P02, P02-T01             |
| P03      | API Badges, Plain-Language Employee UI Surfacing, and Verification | completed | P03, P03-T01, P03-T02    |

<!-- rpi:phase id=P01 -->
## P01: Core Retained Sensor Conflict Propagation and Provenance Grounding

### Context

`src/core/src/zava_forward/core/sensor_view.py` currently includes an uncommitted `conflicts(rows)` helper and attaches `conflicting_readings` and `conflict_notice` inside `capture_source()` (`C1`). However, `grounding()`, `reading_health()`, `advisory()`, `signature()`, and `chat_case_answers.sensor_facts()` still ignore `conflicting_readings` and pick `window[-1]`, and `grounding()` omits synthetic reading provenance fields when non-conflicting (`C2`, `C3`, `C4`, `C7`).

### Intent

Make `sensor_view` and case-chat deterministic facts treat identical-timestamp value conflicts as an explicit non-normal state that routes to human inspection without choosing a reading, while exposing grounded synthetic reading provenance (`provenance_class` and `source_text`) on non-conflicting readings.

### Boundaries

* Included: `src/core/src/zava_forward/core/sensor_view.py`, `src/core/src/zava_forward/core/chat_case_answers.py`, `src/core/src/zava_forward/core/chat_panel.py`.
* Excluded: Telemetry ingestion, SQLite storage tables, simulator generation, and HTTP route wiring.

### Likely Targets

* `src/core/src/zava_forward/core/sensor_view.py`: Propagate `conflicting_readings` into `grounding()`, `reading_health()`, `advisory()`, and `signature()`; add `provenance_class` and `source_text` to `grounding()`.
* `src/core/src/zava_forward/core/chat_case_answers.py`: Populate `sensor.detail` fallback, `sensor.conflict`, and `sensor.source`, and cite reading source text in `_sensor()`.
* `src/core/src/zava_forward/core/chat_panel.py`: Add `"sensor.source"` and `"sensor.conflict"` to `SENSOR_RULE_PATHS`.

### Dependencies

* None.

### Validation Expectations

* Bare `python3 -m mypy`, `python3 -m ruff check .`, and `python3 -m ruff format --check .` in `src/core`.
* `PYTHONPATH=src:tests python3 -m unittest discover -s tests -q` in `src/core`.

### Completion Evidence

* `reading_health({"latest": ..., "conflicting_readings": [...]})["state"] == "conflict"`, `grounding(...)["values"] is None` on conflict, `grounding(...)["provenance_class"]` is populated when non-conflicting, and `test_quality_sensor_grounding.py` preserves exact 3-key `grounding["values"]` compatibility.

### Unresolved Items

* None.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Propagate `conflicting_readings` and reading provenance across `sensor_view.py`

#### Context

Evidence `C1`–`C4` shows `capture_source()` sets `out["conflicting_readings"]` and `out["conflict_notice"]`, which `_view()` passes to `reading_health(out)` and `advisory(out)`. In addition, `test_quality_sensor_grounding.py:52` checks exact dict equality on `grounding["values"]` (`{"temperature_c", "humidity_pct", "observed_at"}`).

#### Intent

Ensure every `sensor_view` projection honors `conflicting_readings` and exposes grounded synthetic provenance on non-conflicting readings without mutating caller inputs or breaking `grounding["values"]`.

#### Boundaries

* Included: `conflicts`, `grounding`, `reading_health`, `advisory`, and `signature` in `src/core/src/zava_forward/core/sensor_view.py`.
* Excluded: Changing `CLASSES` strings, `WATCH` thresholds, or `WINDOW_HOURS`.

#### Likely Targets

* `src/core/src/zava_forward/core/sensor_view.py`:
  * `reading_health(sensors)`: before inspecting `latest`, if `(sensors or {}).get("conflicting_readings")` is truthy, return `dict(state="conflict", text="Retained readings disagree for the same sensor and time. Do not rely on them; use the ordinary quality check.")`.
  * `grounding(sensors)`: if `clashes := (sensors or {}).get("conflicting_readings")` is truthy, collect `conflicting_citations = [k for c in clashes for k in c.get("citation_keys") or []]` and return `dict(out, citation=None, values=None, conflicting_citations=conflicting_citations, text=...)` (reusing the prebuilt `out` dict and `NOT_RETAINED`). When `latest` exists without conflicts, add `provenance_class=latest.get("provenance_class")` and `source_text=CLASSES.get(str(latest.get("provenance_class")), CLASSES["synthetic-unclassified"])` alongside `values`.
  * `advisory(sensors)`: when `(sensors or {}).get("conflicting_readings")` is truthy, return `label="No watch"`, `watch=False`, `reasons=[]`, and `text="Retained readings disagree for the same sensor and time, so no sensor watch is raised. " + WATCH_FRAMING`.
  * `trend_summary()` and `_view()`: return `_trend_base(str(out["conflict_notice"]))` in `_view()` when `out.get("conflicting_readings")` is non-empty, and return `_trend_base("Retained readings disagree for the same sensor and time.")` in `trend_summary()` when `conflicts(ordered)` is non-empty so conflicting 7-day series report `direction="insufficient"` rather than averaging disagreeing values.
  * Leave `signature(sensors)` unchanged (`PC-001`) so the coarse 6-hour proactive scan rate-limit bucket is never invalidated by window conflict churn.

#### Dependencies

* None.

#### Validation Expectations

* Unit assertions in `src/core/tests/test_sensor_view_conflicts.py` and `src/core/tests/test_sensor_view_health.py` plus bare `mypy` and `ruff` in `src/core`.

#### Completion Evidence

* `sensor_view.view()` on conflicting rows reports `health["state"] == "conflict"`, `advisory["watch"] is False`, `conflicting_readings`, and `conflict_notice`; `sensor_view.grounding()` refuses to pick a value on conflict and includes `provenance_class`/`source_text` on clean readings.

#### Unresolved Items

* None.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Surface sensor conflict and reading source provenance in deterministic case chat

#### Context

Evidence `C7` shows `chat_case_answers.sensor_facts(view)` copies `view.get("detail")` (which is `None` when `state == "ok"` even if `conflict_notice` is present!) and does not expose `grounding["source_text"]`. When `grounding["citation"]` becomes `None` on conflict, `_sensor(r)` falls back to `r.fact("sensor.detail")` and otherwise says `"Your role may not include indoor readings."` — which would be misleading for a conflict!

#### Intent

Ensure case chat explains conflicting retained readings and routes to the ordinary manual quality check instead of blaming role permissions or picking one reading, and includes synthetic source framing on clean readings.

#### Boundaries

* Included: `sensor_facts` and `_sensor` in `src/core/src/zava_forward/core/chat_case_answers.py`; `SENSOR_RULE_PATHS` in `src/core/src/zava_forward/core/chat_panel.py`.
* Excluded: Regulatory retrieval or LLM prompt templates.

#### Likely Targets

* `src/core/src/zava_forward/core/chat_case_answers.py`: Set `put("sensor.detail", view.get("detail") or view.get("conflict_notice"))`, `put("sensor.conflict", view.get("conflict_notice"))` when present, and `put("sensor.source", g.get("source_text"))` when `g["citation"]` is present; in `_sensor(r)`'s `if not cite:` branch, check `conflict = r.fact("sensor.conflict")` first (when present, emit plain-language conflict guidance routing to the ordinary quality check plus `r.fact("sensor.not_retained")` so both sentences carry `{case_id}/sensor.*` `decision-rule` citations without claiming no retained readings are shown), and in the clean branch bind `{case_id}/sensor.source` via `r.fact("sensor.source")` inside the `for path in (...)` loop (`PC-003`).
* `src/core/src/zava_forward/core/chat_panel.py`: Add `"sensor.source"` and `"sensor.conflict"` to `SENSOR_RULE_PATHS`.

#### Dependencies

* `P01-T01`.

#### Validation Expectations

* `src/api/tests/test_quality_sensor_grounding.py` passes existing and new conflict/provenance chat tests; bare `mypy` and `ruff` pass in `src/core`.

#### Completion Evidence

* Asking case chat `"What do the indoor humidity sensors show?"` on a conflicted case states the conflict notice and manual quality route with `decision-rule` citations and emits zero numeric sensor reading values.

#### Unresolved Items

* None.

<!-- rpi:phase id=P02 -->
## P02: Quality AI Review Flag Source Provenance and Conflict Gating

### Context

Evidence `C5` and `C6` show `assistants.capture()` already captures `source["sensors"]` and hashes `source:*` and `sensor:*` entries into `snapshot["citations"]`, but `eligible()` can still trigger sensor-only proactive work on conflicted readings, and `review_flag()` neither downgrades conflicted snapshots/arrivals nor exposes per-reading `provenance_class`/`source_text`/`locator`/`content_hash` or a `source_provenance` map across `cited_ids`.

### Intent

Ground Quality AI `review_flag` payloads with complete source provenance for every cited reading and case source, and guarantee conflicting retained readings never trigger sensor-only proactive scans or display autonomous L4 `review-suggested` flags.

### Boundaries

* Included: `eligible` and `review_flag` in `src/core/src/zava_forward/core/assistants.py`.
* Excluded: Changing AI provider adapters, 6-hour `SEAL` rate-limit duration, or human-approval state transitions (`accept`/`reject`).

### Likely Targets

* `src/core/src/zava_forward/core/assistants.py`: Update `eligible()` and `review_flag()`.

### Dependencies

* `P01`.

### Validation Expectations

* `src/api/tests/test_quality_sensors.py`, `src/api/tests/test_quality_sensor_grounding.py`, and `src/api/tests/test_quality_sensors_correlation.py` pass, including consent-withdrawal redaction and same-bucket arrival behavior.

### Completion Evidence

* `review_flag` exposes `readings[*].{provenance_class,source_text,locator,content_hash}`, `cited_provenance_classes`, `source_provenance`, and `invocation_modes`, and returns `status="conflicting-readings"`, `autonomous=False`, `level=None` whenever captured or current readings conflict.

### Unresolved Items

* None.

<!-- rpi:task id=P02-T01 -->
### P02-T01: Gate conflicting readings in `eligible()` and ground `review_flag()` with `source_provenance`

#### Context

`review_flag(task, provenance=(), actionable=False, withheld=False, *, newer_readings=False, current=None)` in `src/core/src/zava_forward/core/assistants.py:278-346` receives `task` (containing `snapshot["citations"]` and `snapshot["sources"]["sensors"]`), `provenance` (invocation events), and `current` (live snapshot in `_view()`).

#### Intent

Attach complete, verifiable source provenance to every Quality AI review flag and block autonomous L4 flagging whenever captured or current retained readings conflict.

#### Boundaries

* Included: `eligible()` (`lines 274-276`) and `review_flag()` (`lines 278-346`) in `src/core/src/zava_forward/core/assistants.py`.
* Excluded: Altering `_withhold_sensors()` contract or `AssistantProvider` wire format.

#### Likely Targets

* `src/core/src/zava_forward/core/assistants.py`:
  * Preserve `def review_flag(task, provenance=(), actionable=True, withheld=False, newer_readings=False, current=None):` defaults and positional compatibility (`PC-001`).
  * In `eligible()`: require `not sensors.get("conflicting_readings")` in the sensor-only proactive branch (`sensors.get("state") == "ok" and sensors.get("readings") and not sensors.get("conflicting_readings") and s["quality"] and not known`).
  * In `Assistants._view()` and `review_flag()`:
    * Keep `if withheld:` first so consent withdrawal returns `status="withheld"`, `readings=[]`, `source_provenance=[]`, and zero sensor IDs.
    * Compute `captured_conflicts = list(sensors.get("conflicting_readings") or [])`, `current_conflicts = list(now_sensors.get("conflicting_readings") or []) if observed else []`, and detect same-bucket current conflict applicability even when a newly-arrived conflicting row adds a new `provenance_class` to `classes` (`PC-001`).
    * In status resolution: after `rejected` and `accepted`, if `state == "ready"` and (`(actionable and captured_conflicts)` or `(same_bucket_eligible and current_conflicts)`), set `status = "conflicting-readings"` ahead of `"not-current"` so `autonomous` is `False` and `level` is `None`.
    * Look up `snap_citations = snap.get("citations") or {}` and `prov_map = sensors.get("provenance") or {}`.
    * Enrich each entry in `readings` with `provenance_class`, `source_text` (`prov_map.get(cls) or sensor_view.CLASSES.get(cls, "")`), `locator` (`(snap_citations.get(k) or {}).get("locator")`), and `content_hash` (`(snap_citations.get(k) or {}).get("content_hash")`).
    * Build `source_provenance` for every `k` in `cited`: `{citation: k, kind: "sensor-reading" if k in known else "case-evidence", locator: ..., content_hash: ..., **(provenance_class, source_text if k in known)}`.
    * Add `cited_provenance_classes=sorted({known[k]["provenance_class"] for k in sensor_cited if known[k].get("provenance_class")})`, `invocation_modes=[str(e.get("mode")) for e in (provenance or ()) if isinstance(e, Mapping) and e.get("kind") == "invocation" and e.get("mode")]` (`PC-006`), and when `status == "conflicting-readings"` or `captured_conflicts`/`current_conflicts` apply, attach `conflicting_readings=clashes` and `conflict_notice` plus conflict-specific `effect` guidance routing to manual quality review.

#### Dependencies

* `P01-T01`.

#### Validation Expectations

* `test_same_ids_and_values_reach_model_and_proactive_flag`, `test_withdrawal_after_model_return_withholds_every_projection`, and new conflict + `source_provenance` grounding tests pass.

#### Completion Evidence

* Every `cited_ids` entry on `review_flag` has a matching `source_provenance` record with snapshot `locator` and `content_hash`, cited readings carry `provenance_class` and `source_text`, and both pre-existing and newly-arrived conflicts produce `status="conflicting-readings"`, `autonomous=False`, `level=None`.

#### Unresolved Items

* None.

<!-- rpi:phase id=P03 -->
## P03: API Badges, Plain-Language Employee UI Surfacing, and Verification

### Context

Evidence `C8`–`C12` shows `/api/cases/<id>/sensors` delegates badge and `next_action` calculation to `sensor_badges.py`, while `web/ops.js` and `web/assistants.js` render `#sensors` and `review_flag`. All `web/*.js` edits are governed by `.github/copilot-instructions.md` Web Development Guidance and `src/api/tests/test_content_standard.py` (`C11`).

### Intent

Expose plain-language `"conflict"` badges, operator `next_action`, conflict notices, and grounded Quality AI reading/source provenance in `src/api`, and verify both `src/core` and `src/api` with focused tests, `mypy`, and `ruff`.

### Boundaries

* Included: `src/api/src/zava_forward/api/sensor_badges.py`, `src/api/src/zava_forward/api/web/{ops.js,assistants.js,chat.js}`, and focused tests in:
  1. `src/core/tests/test_sensor_view_conflicts.py` (canonical unit test file already untracked in worktree)
  2. `src/api/tests/test_quality_sensor_grounding.py` (existing semantic grounding test suite)
  3. `src/api/tests/test_quality_sensors_correlation.py` (existing API/UI/snapshot correlation test suite)
  4. `src/api/tests/test_sensor_staleness_ui_badge.py` (existing badge/UI contract test suite)
  * Test removals: `none`. Maximum test files added/modified: `4` (1 untracked core test file refined + 3 existing API test files extended). No generated files touched.
* Excluded: CSS visual overhauls, framework changes, or modifying unrelated endpoints.

### Likely Targets

* `src/api/src/zava_forward/api/sensor_badges.py`
* `src/api/src/zava_forward/api/web/ops.js`
* `src/api/src/zava_forward/api/web/assistants.js`
* `src/api/src/zava_forward/api/web/chat.js`
* `src/core/tests/test_sensor_view_conflicts.py`
* `src/api/tests/test_quality_sensor_grounding.py`
* `src/api/tests/test_quality_sensors_correlation.py`
* `src/api/tests/test_sensor_staleness_ui_badge.py`

### Dependencies

* `P01`, `P02`, plus loading `web-design-guidelines` and `redesign-existing-projects` skills before editing `web/*.js`.

### Validation Expectations

* `cd src/core && python3 -m mypy && python3 -m ruff check . && python3 -m ruff format --check .`
* `cd src/api && python3 -m mypy && python3 -m ruff check . && python3 -m ruff format --check .`
* Worktree-scoped `unittest` discovery in `src/core` and targeted + regression `unittest` suites in `src/api` (including `test_content_standard`, `test_design_system`, `test_accessibility_baseline`, `test_quality_sensors`, `test_quality_sensor_grounding`, `test_quality_sensors_correlation`, `test_sensor_staleness_ui_badge`).

### Completion Evidence

* Zero `mypy`/`ruff` errors in `src/core` and `src/api`, 100% pass rate on core and API unit tests, and `web-design-guidelines` review clean with `file:line` audit recorded in changes/review artifacts.

### Unresolved Items

* None.

<!-- rpi:task id=P03-T01 -->
### P03-T01: Add `"conflict"` badge/guidance in `sensor_badges.py` and plain-language UI surfacing in `web/*.js`

#### Context

`sensor_badges.py` (`C9`) maps `health.state` to `_HEALTH` and `_NEXT_ACTION`. `ops.js` (`C10`) renders `sensorPanel(v)`, `assistants.js` (`C10`) renders `reviewFlagBlock(f)`, and `chat.js` classifies `RULE_PARTS`. `test_content_standard.py` (`C11`) bans `provenance`, `snapshot`, `gate`, `hold`, `trace`, `envelope` and unowned `BLOCKED_WORDS` in JS string literals.

#### Intent

Render sensor conflicts and Quality AI cited source grounding clearly for housing officers using accessible, plain-language copy that honors Fluent 2 and WCAG 2.2 AA.

#### Boundaries

* Included: `sensor_badges.py`, `web/ops.js`, `web/assistants.js`, `web/chat.js`.
* Excluded: Re-styling CSS tokens or altering non-sensor panels.

#### Likely Targets

* Load `web-design-guidelines` and `redesign-existing-projects` skills before editing `web/*.js`, fetch/refresh current rules (or disclose any network/source limitation), and audit changed JS files against fetched rules (`PC-005`).
* `src/api/src/zava_forward/api/sensor_badges.py`:
  * Add `"conflict": ("Conflicting readings", "Retained readings disagree for the same sensor and time.")` to `_HEALTH`.
  * Add `"conflict": "Do not choose between conflicting readings. Use the ordinary quality check and ask the quality team to check the sensor."` to `_NEXT_ACTION`.
  * In `health_state(view)`, check `"withheld"` and `"unavailable"` first, then return `"conflict"` when `view.get("conflicting_readings")` is truthy or `(view.get("health") or {}).get("state") == "conflict"` BEFORE checking `"offline"`, and in `next_action(view)` check `health == "conflict"` ahead of `freshness == "offline"` when `view.get("state") == "ok"` so context-only (`latest=None`) clashes surface `"conflict"` (`PC-002`).
* `src/api/src/zava_forward/api/web/ops.js`:
  * In `sensorPanel(v)`, guard `v.latest` on line 88 with `if (v.latest && !(v.conflicting_readings || []).length && !v.conflict_notice)` while keeping `sensorTable` rendered so no single reading is promoted as `"Latest:"` (`PC-002`), and when `v.conflict_notice` is present render `h("p", { role: "status", "data-sensor-conflict": "" }, `${v.conflict_notice} Manual route: ${v.manual_route}`)`.
* `src/api/src/zava_forward/api/web/assistants.js`:
  * Add `"conflicting-readings": "Conflicting retained readings: check manually, not an automatic flag"` to `FLAG_TITLES`.
  * In `reviewFlagBlock(f)`: append `${r.source_text ? ` Source: ${r.source_text}` : ""}` on each reading item in `f.readings`; render cited source records `h("p", { class: "muted", "data-flag-sources": "" }, `Cited source records: ${(f.source_provenance || []).map((s) => `${s.citation} (${s.locator})`).join("; ") || "none"}.`)` when `(f.source_provenance || []).length` is non-empty; and render `h("p", { role: "status", "data-flag-conflict": "" }, f.conflict_notice)` when `f.conflict_notice` is present.
* `src/api/src/zava_forward/api/web/chat.js`:
  * Add `"sensor.source"` and `"sensor.conflict"` to `RULE_PARTS`.

#### Dependencies

* `P01-T01`, `P01-T02`, `P02-T01`, `web-design-guidelines`, `redesign-existing-projects`.

#### Validation Expectations

* `test_content_standard.py`, `test_design_system.py`, `test_accessibility_baseline.py`, and `test_sensor_staleness_ui_badge.py` pass; bare `mypy` and `ruff` pass in `src/api`.

#### Completion Evidence

* Annotated `/api/cases/<id>/sensors` payload includes `"conflict"` badge and `next_action` on clashes, and JS panels expose `data-sensor-conflict`, `data-flag-sources`, and `data-flag-conflict` with plain-language copy.

#### Unresolved Items

* None.

<!-- rpi:task id=P03-T02 -->
### P03-T02: Extend focused `src/core` and `src/api` tests and run static/unit verification

#### Context

We must prove both semantic correctness (conflict propagation across `sensor_view`, `chat_case_answers`, `sensor_badges`, `eligible`, and `review_flag` including same-bucket conflict arrival; per-reading and per-citation `source_provenance` grounding; consent-withdrawal redaction of conflict/provenance fields) and regression preservation (`mypy`, `ruff`, UI content/accessibility gates).

#### Intent

Add focused, non-redundant tests that would fail without this change and run all required static and unit checks across `src/core` and `src/api`.

#### Boundaries

* Included: `src/core/tests/test_sensor_view_conflicts.py`, `src/api/tests/test_quality_sensor_grounding.py`, `src/api/tests/test_quality_sensors_correlation.py`, `src/api/tests/test_sensor_staleness_ui_badge.py`.
* Excluded: Adding speculative test frameworks or modifying unrelated test suites.

#### Likely Targets

* Keep strict `mypy` annotations (`-> None`, typed parameters/locals) on all new/modified test methods and helpers (`PC-006`).
* `src/core/tests/test_sensor_view_conflicts.py`: Test `conflicts()`, `reading_health()` (`state == "conflict"`), `grounding()` (`values is None`, `conflicting_citations`, plus `provenance_class`/`source_text` on clean rows), `advisory()` (`watch is False`), and `trend_summary()` / `view()` (`direction == "insufficient"` on conflict).
* `src/api/tests/test_quality_sensor_grounding.py`: Test `review_flag` `source_provenance`, `invocation_modes` (`kind == "invocation"`), and per-reading `provenance_class`/`source_text`/`locator`/`content_hash`, sensor-only `eligible()` conflict suppression, `review_flag` downgrade to `conflicting-readings` (both at capture time and on same-bucket conflicting arrival, including widened `provenance_class`), consent-withdrawal redaction when conflicts existed, and deterministic case-chat `sensor.conflict` / `sensor.source` `decision-rule` routing.
* `src/api/tests/test_quality_sensors_correlation.py`: Verify `/api/cases/<id>/sensors` and Quality AI `review_flag` expose identical reading values, synthetic provenance descriptions, locators/hashes, and `"conflict"` badge / `conflict_notice` correlation, plus `ops.js` (`Latest:` conflict guard) and `assistants.js` source hooks.
* `src/api/tests/test_sensor_staleness_ui_badge.py`: Verify `"conflict"` health badge and `next_action` in `sensor_badges` (outranking stale and context-only `"offline"`, suppressed when withheld/unavailable).

#### Dependencies

* `P01`, `P02`, `P03-T01`.

#### Validation Expectations

* `cd /home/azureuser/source/ama-demo-wt/feat-1288-quality-sensor-ai-2142/src/core && python3 -m mypy && python3 -m ruff check . && python3 -m ruff format --check .`
* `cd /home/azureuser/source/ama-demo-wt/feat-1288-quality-sensor-ai-2142/src/api && python3 -m mypy && python3 -m ruff check . && python3 -m ruff format --check .`
* Worktree-scoped `unittest` runs in `src/core` and `src/api`, including sibling `#1288` suites (`test_quality_sensors`, `test_quality_sensors_c7`, `test_quality_sensors_e1`, `test_quality_sensors_e2`, `test_sensor_trend_summary`) and UI/content suites (`test_content_standard`, `test_design_system`, `test_accessibility_baseline`).
* Touched local browser checks (`checks.quality_sensors_browser_check`, `checks.employee_chat_browser_check`, and `ZF_BROWSER_TESTS=1` chat panel check without `/tmp` scratch paths; explicitly disclose if Chromium/axe is unavailable) (`PC-005`).
* Record validation tier classification (`focused tier`) and `"hosted CI not yet observed (branch unpushed per caller instruction)"` (`PC-005`).

#### Completion Evidence

* All static checks and unit suites exit `0` and are recorded with exact commands and counts in `.copilot-tracking/changes/2026-11-14/quality-1288-sensor-ai-2142-changes.md`.

#### Unresolved Items

* None.
