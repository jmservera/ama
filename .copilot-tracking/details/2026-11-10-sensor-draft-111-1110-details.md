---
title: Issue 111 sensor review draft details and acceptance commands (plan-only phase)
ms.date: 2026-11-10
task_id: 111-sensor-draft-1110
---

## Environment (set at Implement, none run in this phase)

* New venv outside the checkout, for example `/tmp/zf-111-1110/venv`, with `pip install -e src/core -e src/agents -e "src/api[dev]"` from this worktree. The global editable `zava-forward-*` installs resolve to `/home/azureuser/source/ama`, not this worktree (verify the resolved path via `zava_forward.core.sensor_analysis.__file__` or `pip show -f`).
* Constructed synthetic data only. No `ZF_DATA`, credentials, provider, Azure or cloud variable. `ZF_SENSOR_REVIEW_DRAFTS=1` is set only inside tests via `unittest.mock.patch.dict(os.environ, ...)` or the harness process.
* Core commands run from `src/core` with `PYTHONPATH=tests:../agents/tests`; API commands from `src/api` with `PYTHONPATH=tests:../core/tests:../agents/tests`. Raw logs under `/tmp/zf-111-1110/logs/`.

## New test files (dedicated; existing baselines stay unchanged)

### `src/core/tests/test_sensor_review_draft.py`

Production entry `draft_from_retained` is tested only with the unapproved default policy; approvals reach the private seam only. Constructed approval fixture: `RuleApproval(rule_id=RULE_ID, policy_version=ANALYSIS_VERSION, approver_role="SYNTHETIC TEST ONLY", approval_reference="SYNTHETIC-TEST-1")`, module-level comment and class docstring state it is synthetic and not a company or professional approval. Signals come from the pure `derive_signal` over constructed REVIEW rows (humidity above threshold for a persistent run); the retained-store cases build a retained dataset with persistent high humidity because `sensor_consumer_fixture.observations()` is outdoor-derived and may not yield REVIEW (confirm at Phase 1; no change to the existing fixture).

Base class `DraftCases` run against JSON `Store`, SQLite `SqlStore`; subclass `MssqlDraftCases` gated by `ZF_SENSOR_DRAFT_MSSQL=1` against a disposable loopback SQL Server (pattern: `test_sensor_analysis_mssql.py`, `store_at`, `MssqlStore`, `_Conn`).

| Case | Asserts |
| --- | --- |
| default off | env unset: `draft_from_retained` and `read_drafts` deny or report disabled; `cases` body unchanged; no audit entry; no retained read (counting consumer double) |
| role gate | each role outside `DRAFT_ROLES` (all staff roles, Contractor, Application Administrator, resident roles) gets `PermissionError`; `DRAFT_ROLES` equals `REGISTRY["quality-evidence"]["roles"]` |
| default denial without approval | `AnalysisPolicy()` with a REVIEW signal gives `NO_APPROVED_RULE`, no write, no audit |
| approved policy mismatch | wrong `rule_id` or `policy_version` gives `NO_APPROVED_RULE` |
| refusals | INSUFFICIENT, STALE, DECLINED consent, unknown consent, weather-only window, unreadable retained store each give the matching refusal code, zero writes, `priority_effect` stays `NONE` |
| exact lineage | stored draft equals `as_dict(review_task_candidate(...))` field for field (type, queue, home, versions, digest, `task_key`, `approval_reference`, flags) plus lineage; `task_key` is not recomputed in the module (grep assertion that the module has no `sha256` of the key parts) |
| idempotent reopen | second `_record_draft_synthetic` call with same key (different `as_of`, different `at`) returns `existing=True`, list length 1, original `created_at/by/lineage.as_of` unchanged, JSON `store.version` and SQL `rowversion`/`seq` unchanged, audit rows unchanged |
| immutable provenance | changed retained input or policy version gives a second draft with a new key; the first draft's bytes are unchanged |
| bound | the 21st distinct key returns `DRAFT_LIMIT_REACHED`; replay of an existing key at the limit still succeeds |
| restart durability | close and reopen: JSON `Store` on same `live.json`; `SqlStore` on same SQLite file; `MssqlStore` fresh connection. Draft present, digest verifies, replay creates nothing |
| integrity | tamper a stored field directly in the case body: read returns `INTEGRITY_MISMATCH` with only `task_key`; replay with that key does not overwrite it |
| no side effects | before/after equality of case `stage`, `owner_code`, `hazards`, `holds`, `contacts`, `work`, ranking key (`ranking.sql_key`), `handoff`, resident report fields; `assistant_tasks` row count unchanged (no model dispatch); no `handoff` created |
| write failure rollback (JSON) | monkeypatch `save` to raise: pre-call list restored, replay after fix creates exactly one |
| conflict/rollback (SQLite, MSSQL) | open two stores on one database; second store bumps the case `rowversion` between first store's `_case` and `save`; first write raises `ConflictError`; reload shows no draft and no audit row for it; retry creates exactly one; concurrent two-thread same-key attempts end with exactly one draft and no duplicate audit |
| MSSQL specifics | `ZF_SENSOR_DRAFT_MSSQL=1` and also `ZF_SENSOR_MSSQL=1` (the `store_at` fixture keys off the latter) with the `ZF_SQL_*` loopback settings; construct `MssqlStore` explicitly and assert `type(store).__name__ == "MssqlStore"`: same table, plus verify draft survives `_discard()`/reconnect and rowversion path. Skip only by the flag, never silently |
| access projection | sentinel `approval_reference="SYNTHETIC-TEST-SENTINEL"`; `store.detail(case, user)` for every staff role and the Contractor contains no `sensor_review_drafts` key and no sentinel; `store.detail(case)` (internal, user None) still contains it |
| egress sweep | sentinel absent from `home_case_view`, case listing, `export_csv` rows and the AI prompt inputs for the case for every role; any other raw-case egress found by `grep -n "json.dumps(c)\|deepcopy(c)\|dict(c)" src/core/src/zava_forward/core` is added to the list with evidence |
| staff revalidation | revoked, disabled, role-changed, malformed-scope and out-of-scope (`case_ids`, `areas`) users get `PermissionError` on read and write for an existing and a missing case id with the same outcome (no existence probe), no retained read, no write |
| consent recheck on read | stored draft, consent withdrawn then unknown: read returns `consent-withheld` with no summary, lineage or digest; after consent recovers the same draft reads again; no draft mutated |
| future readings | rows dated after `as_of` that would yield REVIEW give `FUTURE_READINGS`, zero writes |
| failure semantics | JSON: save raises, list restored, no audit; audit after save raises, draft kept, audit loss documented. SQL: failure before save, `ConflictError`, and `CommittedReloadError` after commit (outcome unknown, replay idempotent) leave one or zero drafts, never a duplicate, and no committed orphan audit |
| tamper vs text | digest-valid synthetic draft with markup-like summary is the text-rendering fixture; tampered stored body is withheld (`INTEGRITY_MISMATCH`) in a separate case |
| read allowlist | injected unknown key in the stored draft never appears in the view; `draft_digest` not in the view; no `home` address, resident, contact or raw reading text in the view JSON |

### `src/api/tests/test_sensor_review_draft_api.py` (HTTP against a local server on constructed data)

* Flag off: GET `/api/cases/ZF-1/sensor-drafts` returns `{"state":"disabled"}` (200) for permitted roles and 403 for others; POST returns 403.
* Denied callers (including revoked or out-of-scope staff) get the same 403 for existing and missing case ids, with no case detail in the body (POST dispatches before `_case`).
* Contractor and every non-`DRAFT_ROLES` staff role: 403 on both routes; unauthenticated: 401; view-only administrator POST: 403; trusted-proxy POST without CSRF header: 403.
* Flag on, default policy: POST returns 200 `created:false` with the refusal for that fixture per precedence (unavailable, stale, insufficient, no signal, then `NO_APPROVED_RULE`; assert per fixture; served path never approves, never `existing:true`); GET returns an empty list; case body unchanged.
* Seeded synthetic draft (`_record_draft_synthetic` with the synthetic-labelled approval before the request): GET returns it with the label; replay `existing:true` is asserted only on the Python synthetic seam (the served policy is unapproved); malformed windows (non-UTC, not day-aligned, end before start, over 14 days, wrong types, extra keys) return 400 with no write; unknown case 404; `ConflictError` returns the existing 409 text.
* Regression: `/api/cases/ZF-1/sensors` response and `/api/cases/ZF-1` detail are byte-identical before and after for the same state (no new key), existing `test_quality_sensors*`, `test_assistants*`, `test_handoff_api` unchanged.

### Served UI scope check `src/api/checks/sensor_review_draft_browser_check.py`

Modelled on `checks/case_view_ux_browser_check.py` (imports `sign_in`, `scan`, `check`, `main`; local server over constructed `journey_data()`; synthetic draft seeded through `_record_draft_synthetic` with the constructed approval, flag set in the server process; flag set in the server process; one heavy-lock admission). Scope is only the new draft section in the Quality and handover tab of `ZF-1` as Quality Inspector and Retrofit Programme Manager, plus a Retrofit Coordinator and a Contractor negative:

* Flag off: no "Sensor review draft" heading; the only new request is the single `sensor-drafts` GET from the sensor panel returning `disabled`; no `/api/me` change; all other responses unchanged.
* Flag on, no draft: the plain-language empty text and the manual route `manual-sensor-review` are visible.
* Flag on, seeded draft: label "Proposed for a person to review. Not an approved task.", summary, rule id, versions, window, digest start, created by; markup-like text in a digest-valid synthetic summary shows as text; no resident, address or raw reading data in the section text or in the network response.
* Coordinator and Contractor: no section and no `/sensor-drafts` request; direct fetch from the page returns 403.
* axe (`wcag2a/aa/21/22aa`) on `main` with zero serious or critical violations in these states; keyboard order and focus unchanged; 320 px reflow without horizontal scroll; reduced-motion unaffected (no animation added).
* This is an engineering check, not assistive-technology or copy acceptance; record that residual.

## Commands (run at Implement, in this order, local only)

| Step | Command | Pass condition |
| --- | --- | --- |
| V0 | `git fetch && git status --short` and, per shared edge path, `git diff origin/main...HEAD -- <path>` plus sibling-branch diff check | clean; no overlap, else STOP source writes |
| V1 | `python -c "import zava_forward.core.sensor_review_draft as m; print(m.__file__)"` | path under this worktree |
| V2 | from `src/core`: `PYTHONPATH=tests:../agents/tests python -m unittest test_sensor_review_draft -v` | all JSON and SQLite cases ran; MSSQL class listed as skipped only by flag at this step |
| V3 | from `src/core`: `PYTHONPATH=tests:../agents/tests python -m unittest test_sensor_analysis test_sensor_analysis_store test_sqlstore test_taskqueues test_handoff_lifecycle test_sensor_privacy -v` | unchanged baselines OK, no new skips beyond their opt-in flags |
| V4 | disposable loopback SQL Server per the existing local SQL group procedure; from `src/core`: `ZF_SENSOR_DRAFT_MSSQL=1 ... python -m unittest test_sensor_review_draft.MssqlDraftCases -v`, and `ZF_SENSOR_MSSQL=1 ... python -m unittest test_sensor_analysis_mssql -v` | MSSQL class ran, 0 skipped, rollback and conflict cases ran; if Docker or SQL Server cannot start, record the exact blocker and make no SQL claim |
| V5 | from `src/api`: `PYTHONPATH=tests:../core/tests:../agents/tests python -m unittest test_sensor_review_draft_api test_quality_sensors test_assistants test_assistants_dispatch test_handoff_api test_content_standard test_workspace_scripts test_case_journey test_ui_support test_role_screens test_accessibility_baseline -v` | OK, 0 skipped in required scope |
| V6 | `flock -n /tmp/ama-rpi-heavy.lock python -m checks.sensor_review_draft_browser_check` from `src/api` (and `ZF_BROWSER_TESTS=1` for any gated test) | exit 0; lock busy means exit non-zero, no queueing, record pending step |
| V7 | `ruff check` and `ruff format --check` in `src/core` and `src/api`; `mypy` per project config; `node --check src/api/src/zava_forward/api/web/ops.js`; `git diff --check` | exit 0 |
| V8 | `git diff --name-only origin/main...HEAD` allowlist | only the paths in the plan plus own tracking; no `store.py`, `sqlstore.py`, import/exception files or `tools/` |

No blanket `rpi-checks.py --all`, no cloud, no login, no paid model, no private data in this plan. Because the tier is full, the complete local gate and verified external receipt are required before publication by the repository rule; the owner or gate runner schedules that, and the sibling heavy-lock rules apply.

## Acceptance (for Implement and Review)

1. With the flag unset nothing changes anywhere (cases, responses, UI).
2. Approved-rule synthetic candidate persists as one `PROPOSED_UNAPPROVED` draft with the exact candidate identity, versions, digest and `task_key`; replay and restart yield the same single draft; changed input yields a separate draft; old provenance bytes never change.
3. Default served path and every refusal write nothing; stale, missing, weather, declined, unknown consent and unreadable store stay refused; ranking, holds, hazard clocks, ownership, handoffs, assistant tasks unchanged.
4. Only `Quality Inspector` and `Retrofit Programme Manager` can read or write; no other role and no contractor sees any draft field in any response; generic staff detail never carries the key.
5. The existing sensor panel shows the draft with the unapproved label in the real served UI, with the checks above.
6. SQL claims are backed by actual MSSQL runs including conflict rollback; otherwise stated as unproven.

## Residual and unproven after this plan

Real rule approval, R1 to R3 method sign-off, AT and copy acceptance, a real approved-policy source, UI creation control, MSSQL discovery in the pinned gate list (owned by #1300), issue-wide correction balance (UNKNOWN), hosted CI, independent exact-head review.
