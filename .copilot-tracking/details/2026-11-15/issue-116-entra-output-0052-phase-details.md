<!-- markdownlint-disable-file -->
# RPI Phase Details: Issue #116 Provider-Boundary Output Recheck and Document Derivative Controls

## Metadata

* Task ID: issue-116-entra-output-0052
* Task slug: issue-116-entra-output-0052
* Related plan: .copilot-tracking/plans/2026-11-15/issue-116-entra-output-0052-plan.md
* Evidence sources: .copilot-tracking/research/2026-11-15/issue-116-entra-output-0052-research.md, docs/prds/zava-forward-retrofit-programme-demonstrator.md, docs/adrs/0002-pilot-readiness-architecture.md

## Phase Index

| Phase ID | Name                                                                                                                       | Status | Detail sections          |
|----------|----------------------------------------------------------------------------------------------------------------------------|--------|--------------------------|
| P01      | Core Projection-Diff Recheck and Document Derivative/Necessity Guards                                                      | Ready  | P01, P01-T01, P01-T02    |
| P02      | Post-Provider Visibility Rechecks and Document Fallback Wiring Across Tasks, Store, Assistants, Chat, Continuity, and API  | Ready  | P02, P02-T01, P02-T02    |
| P03      | Regression Tests and Focused Tier Validation                                                                               | Ready  | P03, P03-T01             |

<!-- rpi:phase id=P01 -->
## P01: Core Projection-Diff Recheck and Document Derivative/Necessity Guards

### Context

Research (`C1`, `C2`, `C3`, `C10`, `C12`) established that `projection.py` already defines Zava Forward's authoritative default-deny role and field visibility rules (`contractor_detail`, `redact_staff_detail`, `can_see_reason`, `RESIDENT_VIEW_ROLES`, `FINANCE_VIEW`), while `data_protection.py` defines `model_dispatch` and `dispatch_hold` for `raw_document` without a scoped necessity-exception validator or document-level consent/derivative helper.

### Intent

Provide reusable, zero-duplication core helpers in `projection.py`, `data_protection.py`, and `ai.py` that (1) compute exact case and cross-case field values withheld from a role and detect them under Unicode/whitespace normalization, (2) recheck persisted AI `documents[].summary` and `funding.draft` on case read, and (3) fail closed on document AI calls lacking resident consent or an approved derivative / valid scoped necessity exception.

### Boundaries

* Included: `src/core/src/zava_forward/core/projection.py`, `src/core/src/zava_forward/core/data_protection.py`, `src/core/src/zava_forward/core/ai.py`, and `src/agents/src/zava_forward/agents/ai_eval.py`.
* Excluded: Modifying `ai_registry.LEGACY` role tuples or creating any standalone serializer/governance service.

### Likely Targets

* `src/core/src/zava_forward/core/projection.py`: Add projection-diff withheld-value extraction/matching helpers (subtracting all scalar strings still visible anywhere in `projected_detail`) and role-aware rechecking of `documents[].summary` and `funding.draft` inside `redact_staff_detail`.
* `src/core/src/zava_forward/core/data_protection.py`: Add `validate_necessity_exception`, extend `model_dispatch` / `dispatch_hold` (rejecting `"synthetic_safe"` in `actual` mode), and add `document_model_hold`.
* `src/core/src/zava_forward/core/ai.py`: Thread `derivative` and `necessity_exception` through `Ai.look_at` and enforce `document_model_hold` plus `FORBIDDEN` output checks.
* `src/agents/src/zava_forward/agents/ai_eval.py`: Tag `PUBLIC_DOCUMENT` fixture with `ai_derivative="synthetic_safe"` for constructed offline evaluation runs.

### Dependencies

* None.

### Validation Expectations

* Unit checks in `src/core/tests/test_data_protection.py` and full `src/core` test discovery pass with `0` `mypy` or `ruff` issues.

### Completion Evidence

* `projection.py`, `data_protection.py`, and `ai.py` expose typed, reusable helpers exercised by core unit tests.

### Unresolved Items

* None.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Add projection-diff withheld-value helpers and stored AI summary/draft rechecks in `projection.py`

#### Context

`projection.py` (`C1`) explicitly avoids brittle pattern-only redaction because vulnerability reasons, adjustments, notes, and non-status outcomes can be phrased in arbitrary words. Comparing the raw case detail (excluding AI-authored `documents[].summary` and `funding.draft`) against the role-projected detail (`contractor_detail` for contractors, `redact_staff_detail` for staff, or empty projection when access is denied) yields the exact set of case values withheld from `user`.

#### Intent

Add `normalize_visibility_text`, `withheld_case_values`, `withheld_scope_values`, and `contains_withheld_value` in `projection.py`, and recheck stored `documents[].summary` and `funding.draft` inside `redact_staff_detail`.

#### Boundaries

* Included:
  * Normalize candidate and target text with `NFKC`, stripped Unicode format characters (`Cf`), collapsed whitespace, and `.casefold()`.
  * Collect leaf strings from raw case detail (ignoring `documents[].summary` and `funding.draft`) and subtract the set of ALL scalar strings still present anywhere in `user`'s projected detail (`PC-006`) so popped sub-trees sharing visible strings (`"ZF-1"`, `"Survey"`, `"Loft insulation"`, `"Approved"`) never cause false positives; ignore sentinel constants (`""`, `"none"`, `"unknown"`, `REDACTED`, `NOTE_HELD`) and short generic tokens (`< 4` chars unless sourced from explicit high-sensitivity fields `resident.adjustment`, `resident.phone`, `resident.email`, `resident.representative`, `case.reason`, `NOTE_KEYS`, non-status `outcome`, `INTAKE_FIELDS`, or finance/grant identifiers absent from the projected view).
  * Provide `withheld_scope_values(store, user, scoped_case_ids)` using `store.detail(cid)` (raw) vs `store.detail(cid, user)` (projected) (`PC-003`) so multi-case or single-case AI tasks also catch sensitive identifiers/notes/adjustments/contacts leaked from out-of-scope cases in `store.cases`.
  * Inside `redact_staff_detail(user, d)` (`PC-001`): withhold `d["funding"]["draft"]` as `NOTE_HELD` when `user.get("role") not in FINANCE_VIEW` and `d["funding"].get("draft")` is non-empty; compute `forbidden` from incoming unredacted `d` versus redacted `d` (ignoring `documents[].summary` and `funding.draft`); replace `d["documents"][i]["summary"]` or `d["funding"]["draft"]` with `NOTE_HELD` only when matching `forbidden` OR when `doc.get("summary_from_exception")` is `True` and `not can_see_reason(user)`, keeping clean `Grants and Evidence Officer` drafts and `Retrofit Coordinator` / `Quality Inspector` derivative summaries intact.
* Excluded: Changing existing role membership constants (`STAFF_ROLES`, `DEFAULT_REASON_ROLES`, `FINANCE_VIEW`, `RESIDENT_VIEW_ROLES`, `CONTRACTOR_GET`, `CONTRACTOR_POST`).

#### Likely Targets

* `src/core/src/zava_forward/core/projection.py`: Helper functions and `redact_staff_detail` post-pass.

#### Dependencies

* None.

#### Validation Expectations

* Verified by role-projection tests proving legitimate visible facts pass while withheld adjustments, reasons, notes, contacts, finance details, intake fields, and stored AI summaries/drafts are held as `NOTE_HELD`.

#### Completion Evidence

* `projection.redact_staff_detail` holds contaminated `documents[].summary` and `funding.draft` for roles lacking visibility while keeping clean summaries/drafts visible.

#### Unresolved Items

* None.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Enforce approved derivative, scoped necessity exception, and resident AI consent in `data_protection.py`, `ai.py`, and `ai_eval.py`

#### Context

`data_protection.py` (`C10`) currently permits `raw_document` only when `derivative == "reviewed_redacted"` in actual mode and has no representation for a scoped necessity exception. `Ai.look_at` (`C3`) calls `dispatch_hold("raw_document", os.environ)` with no `derivative`, `necessity_exception`, `case_id`, `doc_id`, or `resident_consent` parameters, and omits `FORBIDDEN.search(text)` on returned text. Meanwhile, `PC-002` confirmed `"synthetic_safe"` must be permitted only when `not actual_mode(env)`, `necessity_exception` must thread explicitly through `Ai.look_at` and `data_protection.model_dispatch` / `dispatch_hold` without falsifying `derivative`, and `ai_eval.py` (`PUBLIC_DOCUMENT`) should carry `ai_derivative="synthetic_safe"`.

#### Intent

Implement `validate_necessity_exception`, extend `model_dispatch` and `dispatch_hold`, add `document_model_hold` in `data_protection.py`, enforce them plus `FORBIDDEN` output validation inside `Ai.look_at`, and align `ai_eval.py` (`PUBLIC_DOCUMENT`).

#### Boundaries

* Included:
  * `validate_necessity_exception(exception, *, task="read_document", case_id=None, doc_id=None, actual=False, as_of=None) -> dict[str, str]`: validate mapping with bounded non-empty strings `reference` (`1..120` chars; reject `SYNTH-` prefix when `actual=True`), `approved_by` (`1..120` chars; reject automated/self labels `"ai"`, `"model"`, `"assistant"`, `"system"`, `"auto"`), `reason` (`1..300` chars), `task` (or `scope`) equal to `task` (reject wildcards `"*"`, `"all"`, or mismatched tasks), `case_id` matching `case_id` whenever `case_id` is supplied, `doc_id` matching `doc_id` whenever `doc_id` is supplied, and optional ISO `expires_at` (`YYYY-MM-DD` or ISO timestamp) not expired relative to `as_of` / current UTC date.
  * Extend `model_dispatch` and `dispatch_hold` with optional keyword arguments `necessity_exception=None, task="read_document", case_id=None, doc_id=None, as_of=None` so `c.needs_derivative` permits `derivative == "reviewed_redacted"`, permits `derivative == "synthetic_safe"` ONLY when `not actual_mode(env)` (explicitly held in `actual` mode, `PC-002`), OR permits a valid scoped `necessity_exception`.
  * Add `document_model_hold(doc, env=None, *, case_id=None, resident_consent=None, as_of=None) -> str | None`:
    1. If `resident_consent` is recorded (non-empty) and `.strip().lower() != "given"`, return `"Resident AI data-use consent is not granted; the document remains stored for manual reading and permitted download."`
    2. Evaluate `actual = actual_mode(env)`. If `derivative == "synthetic_safe"` and `actual` is `True`, deny immediately.
    3. When `actual` is `True`, evaluate `dispatch_hold("raw_document", env, derivative=..., necessity_exception=..., task="read_document", case_id=case_id, doc_id=doc_id, as_of=as_of)`.
    4. Whenever `doc` explicitly specifies derivative/exception policy (`ai_derivative` or `derivative` present, OR `requires_derivative=True`, OR `necessity_exception` is present), require `derivative == "reviewed_redacted"`, `(derivative == "synthetic_safe" and not actual)`, OR valid `validate_necessity_exception(..., actual=actual, task="read_document", case_id=case_id, doc_id=doc_id, as_of=as_of)`; otherwise return a deterministic hold reason directing staff to manual reading/download.
  * Update `Ai.look_at` signature with optional keyword arguments `derivative=None, necessity_exception=None, case_id=None, doc_id=None, resident_consent=None`, run `document_model_hold` before any `_chat` call (`PC-002`), and check `FORBIDDEN.search(text)` on provider responses.
  * Update `src/agents/src/zava_forward/agents/ai_eval.py` (`PUBLIC_DOCUMENT` upload metadata) to pass `ai_derivative="synthetic_safe"`.
* Excluded: Changing `Ai.look_at` positional parameters `(self, name, data, mime, off=False)` used by existing callers/tests.

#### Likely Targets

* `src/core/src/zava_forward/core/data_protection.py`
* `src/core/src/zava_forward/core/ai.py`
* `src/agents/src/zava_forward/agents/ai_eval.py`

#### Dependencies

* None.

#### Validation Expectations

* Unit tests in `src/core/tests/test_data_protection.py` verify approved derivative pass, scoped necessity exception pass, wrong `case_id`/`doc_id`/`task`/expired/AI-approved exception rejection, `SYNTH-` rejection in actual mode, resident consent refusal hold, and backward compatibility with existing `model_dispatch` callers.

#### Completion Evidence

* `Ai.look_at` makes `0` provider calls when held and returns `source="template"`, `mode="workflow-only"`.

#### Unresolved Items

* None.

<!-- rpi:phase id=P02 -->
## P02: Post-Provider Visibility Rechecks and Document Fallback Wiring Across Tasks, Store, Assistants, Chat, Continuity, and API

### Context

Research (`C4`-`C9`, `C11`) identified every surface where post-provider outputs, citations, `unresolved` markers, priority `reason` explanations, failed-validation `ai_text` fields, review records (`review`, `live_report`, assistant notes), chat turns/histories, and JSON/CSV exports can pass unauthorized values if input filtering alone fails or if a viewer has narrower role permissions than the actor who triggered generation. It also traced how `Store.add_document`, `Store.read_document`, `Store.get_document`, and `server.py` handle document upload, AI reading, and manual download.

### Intent

Wire `projection` withheld-value rechecks across all six output/export surfaces and wire document derivative/exception metadata + manual fallback guarantees through `ai_tasks.py`, `store.py`, `assistants.py`, `chat_isolation.py`, `chat_panel.py`, `chatthreads.py`, `continuity.py`, and `server.py`.

### Boundaries

* Included: `ai_tasks.py`, `store.py`, `assistants.py`, `chat_isolation.py`, `chat_panel.py`, `chatthreads.py`, `continuity.py`, and `server.py`.
* Excluded: Frontend layout redesign, database schema migrations (JSON document metadata and existing columns carry all fields cleanly), or altering `ai_registry.LEGACY`.

### Likely Targets

* `src/core/src/zava_forward/core/ai_tasks.py`: Post-provider visibility & live-permission rechecks in `finish`, `run_text_task`, `run_document`, `review`, and `live_report`.
* `src/core/src/zava_forward/core/store.py`: Fix `_facts` reason leak; add withheld-value rechecks in `ai_priority` and `_rec_view`; support derivative/exception metadata and redacted derivative dispatch in `add_document` and `read_document`; pass `user` in `ai_live_report`.
* `src/core/src/zava_forward/core/assistants.py`: Post-provider output visibility check in `complete` and viewer-scoped output/note rechecks in `_view`.
* `src/core/src/zava_forward/core/chat_isolation.py`, `chat_panel.py`, `chatthreads.py`: Upgrade `_withheld` to full projection-diff + cross-case check, check citations in `ChatPanel._ask`, and scrub resumed thread messages when visibility changes.
* `src/core/src/zava_forward/core/continuity.py`: Require reason + resident + finance visibility for full continuity export.
* `src/api/src/zava_forward/api/server.py`: Pass `u` to `s.ai_live_report(u)`, recheck resumed chat threads on `GET /api/chat/threads/{tid}`, and pass optional derivative/exception metadata on `/api/cases/{id}/upload` and `/api/cases/{id}/read-doc`.

### Dependencies

* P01 (`projection.py` and `data_protection.py` helpers).

### Validation Expectations

* Existing and new `src/core`, `src/api`, and `src/agents/tests/test_ai_eval.py` tests pass with `0` regressions.

### Completion Evidence

* All six output/export surfaces and all document derivative/fallback paths enforce role visibility and manual continuity end-to-end.

### Unresolved Items

* None.

<!-- rpi:task id=P02-T01 -->
### P02-T01: Enforce post-provider output, citation, explanation, error, and review-record rechecks in `ai_tasks.py` and `store.py`, plus document metadata/fallback preservation

#### Context

1. `ai_tasks.finish` (`C4`) currently returns `dict(result, ...)` including raw `ai_text` on validation failure, echoes raw `unresolved` `[[...]]` strings, and does not check `result["text"]` or `cites` against `projection.withheld_scope_values`.
2. `Store._facts` (`C5`) interpolates `c["reason"]` even when `reason_ok=False`.
3. `Store.ai_priority` and `Store._rec_view` (`C6`) do not recheck item `reason` explanations or `cites` against `user`'s current role visibility.
4. `ai_tasks.live_report` (`C4`) returns `reviewer_reasons` regardless of `projection.can_see_reason(user)`.
5. `Store.add_document` and `Store.read_document` (`C5`) need optional `ai_derivative` (`"intact"` / `"reviewed_redacted"`), bounded `derivative_text`, `requires_derivative`, and `necessity_exception` support, sending `derivative_text.encode("utf-8")` when `ai_derivative == "reviewed_redacted"` and `derivative_text` is present while preserving intact bytes in `docstore` for `get_document` and preserving existing human `doc["summary"]` when AI is denied.

#### Intent

Close all leak vectors in `ai_tasks.py` and `store.py` and wire document derivative/exception/consent guards with full manual fallback preservation.

#### Boundaries

* Included:
  * `ai_tasks.finish` (`PC-003`, `PC-004`): Keep `r["ai_text"] = text` in `Ai.run`; inside `finish`'s `publish(late)` callback BEFORE `env`, `add_record`, `publish_output`, and `statement_sources`, verify `user.get("role") in projection.STAFF_ROLES` and `all(store.detail(cid, user) is not None for cid in case_ids)` and compute `forbidden = projection.withheld_scope_values(store, user, case_ids)`. Scrub `unresolved` markers matching `forbidden`. When permission fails or `r["text"]` (when `r["source"] == "ai"`), `cites`, or raw `[[...]]` markers match `forbidden`, rebind `r` to a template fallback (`source="template"`, `model=None`, `mode="workflow-only"`, `validated=False`, `verified=True`, `text=workflow_text`, `reason="model output withheld by role visibility check; use the manual route"`), clear `cites=[]` and `unresolved=[]`, and set `ai_output = None` whenever `ai_output` matches `forbidden` or `ai.FORBIDDEN` (preserving clean `ai_output` on permitted-scope quarantine, financial-attribution, and unverified records). Omit `"ai_text"` from the public dictionary returned by `finish()`.
  * `ai_tasks.review` & `ai_tasks.live_report(store, user=None)` & `Store.ai_live_report(self, user=None)` (`PC-005`): Verify active staff permission and current case visibility on `review`, scrub returned `rec` (`ai_output`, `override_text`, `review_evidence`) against `withheld_scope_values` and `can_see_reason(user)`, and in `live_report(store, user)` enforce `MANAGER_ROLES` when `user is not None` and replace `reviewer_reasons[].reason` with `projection.NOTE_HELD` when `not projection.can_see_reason(user)`.
  * `Store._facts`, `Store.ai_run`, and `Store.funding_draft` (`PC-001`, `PC-003`): Include `c["reason"]` in `_facts` only when `reason_ok` is `True`; make `Store.ai_run` fallback `tmpl` role-safe when `not projection.can_see_reason(user)` (using `projection.status_only(c["waiting_on"], self.status_line(c))` and masking `outside {r['unavailable']}`); and pass `self._facts(c, False)` in `Store.funding_draft` (`store.py:1182`) so shared `FINANCE_VIEW` drafts never pull reason-only facts.
  * `Store.ai_priority` & `Store._rec_view` (`PC-003`, `PC-004`): Reject AI priority outputs in `valid(text)` if any item `reason` or `cites` contains `withheld_scope_values` for `user`, clear `ai_output` if `r.get("ai_text")` contains `withheld_scope_values` or `ai.FORBIDDEN`, and in `_rec_view(rec, user)` re-verify case visibility (`self._visible(c, user)`), filter `cites` against `ai_tasks.source_labels(c, projection.can_see_reason(user))`, scrub `ai_output` against `withheld_scope_values`, and replace item `reason` (and `final_items[].reason`) with `projection.NOTE_HELD` if it contains values withheld from `user`.
  * `Store.add_document` & `Store.read_document` & `ai_tasks.run_document` (`PC-001`, `PC-002`, `PC-006`): Validate optional derivative/exception fields inside `with change_provenance.operation(...)` after `isinstance(metadata, Mapping)` guarding before `self.docstore.put(...)` (`PC-006`) so `metadata=None` preserves `ValueError` semantics without orphan blobs. Support `ai_derivative` / `derivative`, bounded `derivative_text` (`<= 20_000` chars), `requires_derivative`, and `necessity_exception` on `add_document` and `read_document`. Evaluate `data_protection.document_model_hold` (including `case["resident"].get("ai_data_use_consent")`). When held, make `0` provider calls, return `source="template"`, `mode="workflow-only"`, `manual_available=True`, `approval="Not reviewed"`, `instruction_status="Not an instruction"`, and preserve any existing non-empty `doc["summary"]` (setting `"The file is stored. It is not sent to AI; add a short note about what it is."` only when `doc["summary"]` was empty). When `ai_derivative == "reviewed_redacted"` and `derivative_text` is present, pass `derivative_text.encode("utf-8")` with `"text/plain"` to `run_document` / `Ai.look_at` while keeping intact raw bytes in `docstore` for `get_document`; record `doc["summary_from_exception"] = bool(used_exception)` when AI runs under a `necessity_exception` (`PC-001`).
* Excluded: Changing contractor `403` rules or malware-quarantine download blocks in `get_document`.

#### Likely Targets

* `src/core/src/zava_forward/core/ai_tasks.py`
* `src/core/src/zava_forward/core/store.py`

#### Dependencies

* P01-T01, P01-T02.

#### Validation Expectations

* Mocked provider canary injections in `briefing`, `draft_case`, `funding_draft`, `read_document`, `ai_priority`, validation failures, and `ai_live_report` are withheld/scrubbed, and denied `read_document` calls make `0` provider requests while `get_document`, `detail`, `draft`, consent, and hazard routes remain operational.

#### Completion Evidence

* Unit and API tests confirm zero unauthorized field leaks and preserved manual/download workflows across JSON and SQLite stores.

#### Unresolved Items

* None.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Enforce post-provider and read/export visibility rechecks in `assistants.py`, `chat_isolation.py`, `chat_panel.py`, `chatthreads.py`, `continuity.py`, and `server.py`

#### Context

1. `assistants.py` (`C7`) shares proposal records across multiple staff roles (`REGISTRY[capability]["roles"]`) and exports them via `/api/assistants/proposals.csv` (`server.py:701`).
2. `ChatIsolation._withheld` (`C8`) only checks `TOOLISH` and `resident["adjustment"]`, and `GET /api/chat/threads/{tid}` (`C11`) resumes stored messages without rechecking case access or current role field visibility.
3. `continuity_export` (`C11`) allows any `MANAGER_ROLES` caller to request `full=True` when `can_see_reason(user)` is true, even if a role lacks `RESIDENT_VIEW_ROLES` or `FINANCE_VIEW`.
4. `server.py` (`C11`) calls `s.ai_live_report()` without `u`, and `/api/cases/{id}/upload` + `/api/cases/{id}/read-doc` need clean optional pass-through for derivative and necessity-exception fields.

#### Intent

Enforce role/field visibility rechecks across assistants (including CSV export), chat replies/citations/resumed threads, continuity export, and HTTP handlers in `server.py`.

#### Boundaries

* Included:
  * `assistants.py`: In `complete`, recheck `output` (`summary`, `findings[].text`, `unknowns`) against the union of withheld case values across `REGISTRY[current["capability"]]["roles"]` (so a shared proposal cannot embed fields forbidden to one of its target roles; if violated, fail validation cleanly as withheld proposal). In `_view`, recheck `body["output"]` against the reading `user`'s withheld values on case `c` (if violated, replace `output` with `dict(WITHHELD_OUTPUT)` and set `actionable=False`, `relied_on=False`), and when `not projection.can_see_reason(user)`, replace non-empty `verification.note`, `review.note`, and `provenance` event notes with `projection.NOTE_HELD`.
  * `chat_isolation.py`, `chat_panel.py`, `chatthreads.py` (`PC-005`): Upgrade `ChatIsolation._withheld(user, thread, reply)` to check `TOOLISH` plus `projection.withheld_scope_values(self.store, user, [case_id] if case_id else [])`; check resolved citation snippets as well as `answer` in `ChatPanel._ask`; add `ChatIsolation.scrub_thread(user, thread)` raising `ChatNotFound` (`404`) whenever a case-bound thread's `case_id` is missing or no longer visible to `user` (`self.store.detail(cid, u) is None`) and replacing assistant message `content`/`evidence` containing withheld values with `projection.NOTE_HELD` when the case remains visible under narrowed field visibility; apply the same `ChatNotFound` + assistant-message withholding in `chatthreads.py:chat_resume` when `t.get("case_id")` is in `self.cases` and `user.get("role")` is present.
  * `continuity.py` (`PC-005`): Require `projection.can_see_reason(user) and user.get("role") in projection.RESIDENT_VIEW_ROLES and user.get("role") in projection.FINANCE_VIEW` before returning `scope="full"` (otherwise returning `limited_export(bundle)`), AND project `ai_records` and `assistant_proposals` in the full-export branch against `projection.withheld_scope_values` for `user`.
  * `server.py`: Pass `u` to `s.ai_live_report(u)` on `GET /api/ai/report`; call `c.scrub_thread(current, thread)` on `GET /api/chat/threads/{tid}` for non-regulatory threads; forward optional `ai_derivative` / `derivative`, `derivative_text`, `requires_derivative`, and `necessity_exception` fields on `/api/cases/{id}/upload` and `/api/cases/{id}/read-doc`.
* Excluded: Changing assistant capability role lists or chat request field allowlists.

#### Likely Targets

* `src/core/src/zava_forward/core/assistants.py`
* `src/core/src/zava_forward/core/chat_isolation.py`
* `src/core/src/zava_forward/core/chat_panel.py`
* `src/core/src/zava_forward/core/chatthreads.py`
* `src/core/src/zava_forward/core/continuity.py`
* `src/api/src/zava_forward/api/server.py`

#### Dependencies

* P01-T01, P01-T02, P02-T01.

#### Validation Expectations

* API tests verify `/api/ai/report`, `/api/assistants/proposals`, `/api/assistants/proposals.csv`, `/api/chat/threads/{tid}`, `/api/cases.csv`, `/api/continuity/export`, `/api/cases/{id}/upload`, `/api/cases/{id}/read-doc`, and `/api/docs/{cid}/{did}` enforce role visibility and document derivative/manual-fallback rules.

#### Completion Evidence

* Zero unauthorized canary strings appear across assistant JSON/CSV, chat replies/threads, live AI reports, or exports.

#### Unresolved Items

* None.

<!-- rpi:phase id=P03 -->
## P03: Regression Tests and Focused Tier Validation

### Context

Issue #116 requires local-testable proof of both increments under the focused validation tier (`unittest` in `src/core` and `src/api`, plus `mypy` and `ruff` check/format, without running `tools/rpi-checks.py --all`).

### Intent

Add high-signal unit and HTTP regression tests in the existing canonical test files and verify clean execution across all focused suites, type checks, and lint/format checks.

### Boundaries

* Included: `src/core/tests/test_data_protection.py`, `src/api/tests/test_ai_tasks.py`, and `src/api/tests/test_role_endpoint_inventory.py` (`<= 18` focused test methods added; `0` removals; `0` new test files).
* Excluded: Running `tools/rpi-checks.py --all` or adding redundant constant/trivial tests.

### Likely Targets

* `src/core/tests/test_data_protection.py`: Unit tests for `validate_necessity_exception`, `model_dispatch` / `dispatch_hold` with necessity exceptions, and `document_model_hold` (approved derivative, scoped exception, wrong case/doc/task/expired/AI-approved/`SYNTH-` rejection, and resident consent hold).
* `src/api/tests/test_ai_tasks.py`: End-to-end store and HTTP tests proving (1) post-provider canary leaks in AI task outputs, unresolved `[[...]]` citations, priority `reason` explanations, failed-validation `ai_text` error responses, stored `documents[].summary` / `funding.draft`, `ai_live_report` (`Programme Support Officer` vs `Retrofit Programme Manager`), assistant proposals + `/api/assistants/proposals.csv`, chat replies/citations/resumed threads, and continuity export are withheld; and (2) document AI processing requires approved derivative (`reviewed_redacted`, sending `derivative_text` only) or valid scoped necessity exception and resident consent, while upload/storage, manual case reading, permitted staff download, proposal-only boundaries, resident consent updates, and independent manual/hazard routes remain available when denied (across JSON and SQLite).
* `src/api/tests/test_role_endpoint_inventory.py`: Role-inventory assertions verifying contractor `403` default-deny on document/AI/review/export routes, `Programme Support Officer` `NOTE_HELD` enforcement on `/api/ai/report` and `limited` scope on `/api/continuity/export`, and cross-role visibility protection when stored case summaries/drafts or assistant notes are read by non-reason/non-resident/non-finance staff roles.

### Dependencies

* P01, P02.

### Validation Expectations

* `PYTHONPATH=../core/tests:../agents/tests python3 -m unittest discover -s tests -q` in `src/api` exits `0`.
* `python3 -m unittest discover -s tests -q` in `src/core` exits `0`.
* `PYTHONPATH=../core/tests python3 -m unittest discover -s tests -p 'test_ai_eval.py' -q` in `src/agents` exits `0`.
* `python3 -m mypy` on `src/core` and `src/api` exits `0`.
* `python3 -m ruff check .` and `python3 -m ruff format --check .` exit `0`.

### Completion Evidence

* Exact command exit codes and test counts recorded in `.copilot-tracking/changes/2026-11-15/issue-116-entra-output-0052-changes.md`.

### Unresolved Items

* None.

<!-- rpi:task id=P03-T01 -->
### P03-T01: Add unit and HTTP regression tests in `test_data_protection.py`, `test_ai_tasks.py`, and `test_role_endpoint_inventory.py` and run focused validation

#### Context

All acceptance criteria for Increment 1 (output, citation, explanation, error, review-record, and export permission/visibility recheck) and Increment 2 (document approved derivative or scoped necessity exception + manual storage/reading/download/consent/proposal-only/hazard availability on denial) must be verified by tests that fail without the changes and run completely offline.

#### Intent

Author focused regression tests across the three canonical test suites and execute the complete focused validation tier.

#### Boundaries

* Included: `src/core/tests/test_data_protection.py`, `src/api/tests/test_ai_tasks.py`, `src/api/tests/test_role_endpoint_inventory.py`, and focused `unittest` / `mypy` / `ruff` runs.
* Excluded: `tools/rpi-checks.py --all`, browser tests, or live cloud dependencies.

#### Likely Targets

* `src/core/tests/test_data_protection.py`
* `src/api/tests/test_ai_tasks.py`
* `src/api/tests/test_role_endpoint_inventory.py`

#### Dependencies

* P01-T01, P01-T02, P02-T01, P02-T02.

#### Validation Expectations

* Zero test failures, zero `mypy` errors, zero `ruff` lint or format issues.

#### Completion Evidence

* Passing test and static-analysis runs captured in the implementation changes artifact.

#### Unresolved Items

* None.
