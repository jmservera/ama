---
title: Issue 97 phase details
description: Task-level evidence, boundaries and completion expectations
ms.date: 2026-10-17
---

## Metadata

Task ID: 97. Slug: form-schema-staging-97.
Plan: .copilot-tracking/plans/2026-10-17/form-schema-staging-97-plan.md.
Research: .copilot-tracking/research/2026-10-17/form-schema-staging-97-research.md.
Initial direction: bounded core/API data engineering; no new authority or downstream workflow.

## Phase Index

| Phase | Status | Tasks |
| --- | --- | --- |
| P01 | Complete; original core missing contract and real HTTP 404 observed | P01-T01 |
| P02 | Complete; registry, staging, persistence, API and component docs | P02-T01, P02-T02 |
| P03 | Complete; final core 551/API 565 test runs and static checks | P03-T01 |

<!-- rpi:phase id=P01 -->
## P01: Fail-before contract

<!-- rpi:task id=P01-T01 -->
### P01-T01: Focused external tests

Use temporary synthetic DATA fixture, install editable src distributions first, test public core functions and actual HTTP endpoints. Capture failures caused by missing form contract, not absent dependencies. Own two new test files only. No source/UI/private dataset changes. Completion evidence is literal failing command output/counts in changes artifact.

<!-- rpi:phase id=P02 -->
## P02: Data contract

<!-- rpi:task id=P02-T01 -->
### P02-T01: Registry and staging

Evidence C4-C6: document hashes/versions/scans already exist. Add one `forms.py` domain module operating against a small Store protocol, not a second store. `form_schemas` shared document uses checked `_proc_write`; per-case `form_staging` holds immutable batches with generated IDs/actor/time, exact schema digest/version and source snapshots. Reuse `ai_registry.digest`, existing staff roles and scanner. Registering a schema never approves it. Source authority is schema policy, never a new source truth claim.

Text and CSV supplied candidate locations must resolve exactly to raw source text; preserve alternatives independently. OCR imports contain parser/version/model/route/error metadata with explicit unverified status and no provider call. No rule execution/field acceptance. Unsupported source types or decode/CSV problems create an owned manual-recovery batch with no values. Validation errors never partially append candidates. Return defensive copies.

SQL tests cover reopen, second-process sync and controlled concurrent failure. Restore local mutations on failed saves and preserve existing database exceptions. MssqlStore inherits shared-document logic; do not claim live Azure behavior from SQLite.

<!-- rpi:task id=P02-T02 -->
### P02-T02: API and docs

Add GET/POST `/api/form-schemas`; GET `/api/cases/{case_id}/form-candidates`; POST `/api/cases/{case_id}/form-candidates`. Use existing authentication, explicit staff/document/Finance source checks, consistent 400/403/404/409 errors and source-store 502. No generic case detail exposes candidate raw data. Explicit service failure path must not look like success.

Component docs describe exact payloads, approval/authority limits, parser verification and manual recovery. Add one routing row/index and append-only log entry, preserving concurrent entries. No PRD/addendum rewrites.

<!-- rpi:phase id=P03 -->
## P03: Evidence reconciliation

<!-- rpi:task id=P03-T01 -->
### P03-T01: Validation

Run actual focused tests and HTTP fixture; then core/API component unit suites, `ruff check .`, `ruff format --check .`, and `mypy` from each component using own pip venv. No Docker escalation. Existing live-only skips remain skips; unrelated failures remain explicitly reported, not silently fixed. Record exact counts and commands, mark tasks complete only against evidence. Reconcile plan/details/changes/state before exactly one Review. Code and all artifacts must be committed and pushed with Refs #97 PR targeting main, no closing keyword or merge.

## Unresolved Acceptance

Actual approved schema/template, funding route and human authority are not supplied. No fixture can resolve this. This implementation provides unapproved schema and staged-candidate mechanics only, not approved preparation. Full PRD AC-046/047/053 and parent #96 remain open.

## Implementation-time integration amendment

P03's first full API suite failed exactly one existing assertion: the endpoint inventory requires every new route to be listed. Add GET/POST registry and candidate paths and the dynamic `form-candidates` action to existing `test_role_endpoint_inventory.py`. This is required integration coverage, not a new test module, removed test, scope expansion or reason to repeat critique. Re-run the inventory and API suite.

## Final Critique Corrections

PC-001: All registry/candidate operations require the registered current actor to have all existing Finance-view, resident-record-view and reason-view rights. This intentionally conservative intersection avoids arbitrary raw text bypassing restricted fields. Schema policies never grant rights. Recheck identity and rights on retained reads; source still must exist, be clean, and belong to the case. No raw batches in generic detail, error messages or audit. Test role revocation, contractor/unknown/reason-restricted users.

PC-002: Schema request exact keys: `id`, `version`, `form_type`, `template`, `reviewer`, `funding`, `rule_refs`, `fields`. Template/ref objects contain `id`, `version`, `evidence_ref`. Funding object is `{status, scheme_id, route, evidence_ref}` with status Unknown, Not applicable or Evidenced; funding types cannot be Not applicable; non-funding types explicitly choose Not applicable or a required evidenced/unknown association. Evidenced is supplied reference metadata, never approved scheme authority. Fields contain `id`, `section_id`, `type`, `unit`, `options`, `required`, `required_when`, `source_authority`, `evidence_required`, `calculation_ref`, `category`. Categories declaration/signature/attestation/consent/approval are always human-only and cannot receive candidates; ordinary `value` fields can. Source policy contains kind/rank/evidence_ref; it is explicitly unapproved metadata, not source authority. Conditions are `{field_id, equals}` data only. Versions are strict positive sequential integers; duplicates rejected with no overwrite. Approval/audit keys are server-only.

PC-003: Stage request exact keys: `schema_id`, `schema_version`, `document_id`, `processing`, `candidates`. Processing `{kind, parser, parser_version, model_version, route_evidence, error_record}` is supplied/unverified assertion, never attested execution. Kinds text/csv/ocr. Text uses strict UTF-8 without newline normalization; locator `{start,end}` is zero-based Unicode code-point half-open offsets. CSV uses Python csv strict reader, UTF-8, 1-based `{row,column}`, includes header, preserves quoted/multiline cell content as raw value. OCR locator `{page,region}` is asserted, not validated against pixels; route evidence/error record required, all remain explicitly unverified. Server records separate verifier `form-source-locator-1`, location match result and actual byte hash. Decode/unsupported/CSV parse failures produce owned manual recovery only.

PC-004: Include registry and candidate non-conflict save/audit fault injection, local and reopened equality, no failed audit/body and no replay after next successful operation. The form operations restore operation-local in-memory mutations on failures and rethrow; API logs unexpected failure and returns 503, never manual-success fallback.

PC-005: PRD v0.12.0 exercise-planning acceptance on 2026-10-10 is sufficient baseline direction. It does not approve a form schema or operational release. No renewed PRD signature requested.
