---
title: Issue 84 phase details
description: Evidence-based completion expectations
ms.date: 2026-10-15
---

Task ID: 84. Slug: stock-reconciliation-84.

## P01

P01-T01: Use typed core helpers for strict comparison shape; allowlist only EPC,
home type and build year, no resident/free-text health fields. Require two
nonidentical, source-bound values with date/version/validation metadata and a
registered staff query owner. Append history; no source wins automatically.
Store orchestrates lock/audit/save; SQL inherits existing case persistence.
Technical gate includes unresolved conflict owner, with no silent cohort removal.

P01-T02: Preserve signoffs.py and its four role mappings (exercise proposal,
not attested competence). Registered actor identity must match staff; body
cannot supply approval identity. Validate affects and note before mutation;
require explicit nonempty unique affected list when supplied. History records
email, role, design version. Building approval and coordination reuse building
blockers, every approval reuses hazard holds. No new consent or handoff engine.

P01-T03: A typed support helper separates known support from coverage Unknown.
Absent/null priority flag and adjustment are never interpreted as false/None.
No automatic health inference or new ranking weight. All ranking entry points,
SQL-derived summary, staff detail and linked filters handle incomplete inputs.
Contract: `support_status` is Yes if priority_support is exactly true or a
nonempty adjustment other than None/Unknown is recorded; No only for exactly
false plus the explicit string None; otherwise Unknown. `support_coverage` is
Unknown if either input is absent/null/invalid, including mixed positive cases.
Compatibility `support`/needs_notice stays Boolean, true only for observed
positive evidence; never coerce the display string. Unknown sorts in the
existing nonpositive support bucket, then waiting/stage/ID decide; no weight
is invented. Detail, redaction, list, stats, visits, filters and AI facts use
the same helpers; stats separately counts incomplete coverage.
Use meta support_encoding=1 for an idempotent existing-database derived-column
refresh through existing portable hooks, without rewriting case assertions,
audit, consent or ranking policy. Test a legacy current-policy database with
stale support/rkey, reopen twice, and compare JSON/SQL lists, filters and cursors.
Evaluate comparison holds before missing_items' no-design return and also
before new sign-off approval. Test no-design and previously-signed cases;
preserve history and allow independent hazard intake.

## P02

P02-T01: Add staff-only POST /api/cases/{id}/stock-reconciliation with existing
authentication and error mapping. Response is the role-projected case detail.
Read-only staff panel compares labelled source evidence, both values, metadata
and owner, with Unknown states and no implied resolution or eligibility pass.
Use DOM text nodes and existing headings; no raw HTML or inaccessible widgets.

P02-T02: At most two new modules/24 methods, no test removal. Core exercises
valid/invalid comparisons, exact source metadata, unknown flags, deterministic
ranking, JSON/SQL persistence, affected-only reapproval, authenticated sign-offs,
and unchanged home consent/building/handoff/hazard authority. API tests run a
loopback HTTP server with synthetic fixture and SQL store, exercise login,
400/401/403 responses, staff/contractor projections and static app delivery.
No private generated operating data or secrets are read.

## P03

P03-T01: Record each actual command and result in the changes artifact, including
missing-tool probes and corrective pip installation. Run targeted tests first,
then every src project suite, lint/format/mypy and node syntax checks.
Attempt Docker without privilege escalation; rely on CI for unavailable image
and SQL Server evidence. Do not claim real AI execution from a mock/local check.
Use existing Playwright runtime if available for a synthetic rendered case
check: both values/metadata/owner, Unknown support, second-case navigation
without stale evidence, heading/keyboard access. If the browser is unavailable,
record rendered-view validation explicitly as unmet, not passed by static HTTP.

P03-T02: Core/API README document shapes, boundaries and evidence gaps.
Reference index links those durable contracts; append log entry without
rewriting history or memory. No regulatory claim or snapshot change.

P03-T03: Reconcile plan/details/changes, run Review once with separate execution
and outcome, route findings to later work. Resolve authenticated GitHub identity,
configure local privacy-safe email, Conventional Commit with required trailer,
push only named topic and create main PR using Refs #84. Leave unmet criteria
unticked; no merge.
