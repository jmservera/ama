---
title: Home chat changes
description: Implementation evidence for issue 214
ms.date: 2026-10-16
---

## Starting state

Full plan P01-P03; clean feat/regulatory-home-chat-214 based on origin/main;
no existing PR. Source writes restricted to src. Documentation exceptions:
requested RPI evidence and docs/reference/log.md. No active implementation
blocker. Validation and operational gaps remain as stated in the plan.

## P01-T01: Cited answer boundary

Core regulatory_chat builds bounded source/card and role-minimised fact
snapshots, reusing citation_eligibility. Agents regulatory_chat renders exact
attributed excerpts in a fixed template, with finite hazard/automated-decision
purposes and pre-retrieval legal/unsupported refusal. No provider path is wired.
Full versioned JSON citation envelopes and hash-bound observed facts persist in
existing isolated chat messages. Answer pairs use one repository transaction.

## P02-T01: Explicit doubt and panel

API adds synthetic-only regulatory routes, blocks generic chat bypass and
role-changed history, and retains independent rules/alerts. Named provisioned
Juan Manuel Servera receives only the selected pair in his own thread, with
idempotent sender receipt and transaction rollback. JSON uses a pre-image on
failure. UI supports cited turn, historical resume, doubt and owner inbox with
safe DOM text and status announcements.

## Validation and implementation refinements

Initial 10 core tests passed after correcting incomplete synthetic hazard
fixtures; five agents tests pass including 3/3 cited and 10/10 refusal evaluation.
Four real local HTTP tests pass after resolving a meaningful repository finding:
SqlStore caches staff indefinitely. Regulatory admission/recipient resolution
now re-read SQL staff directly so role revocation takes effect without restart.
This is a tightly coupled guard correction, not a general staff-store refactor.
Agents project mypy passes. API mypy found missing installed Playwright stubs
and one new test annotation; install the existing declared tool and fix the
annotation, without changing dependency versions.

## P03-T01: Deterministic evaluation and regressions

Added 23 initial focused tests across core/agents/API plus later conservative
unsupported-topic-question coverage. Frozen evaluator runs twice identically:
3/3 exact cited answers, 10/10 expected refusals. Baseline contains the same
actual card/provision links: zero home fragments versus six joined fragments
over three answers, three structural lookups versus one joined request.
This is not a staff-time or actual-model result. The recorded report is checked
by the agents test, not a handwritten success assertion.

Core chat/source/rule regression selection: 105 tests passed. Agents selection:
43 passed. API selection: 98 ran, 16 existing optional skips, remaining passed.
Expected rule-store-unavailable logs belong to existing outage exercises.
Core/agents/API project ruff, format and mypy passed before final small edits;
final rerun remains required. Local loopback HTTP covers actual new endpoints.
No browser/human, Azure, real-model or continuing-stock result is claimed.

## Immediately relevant guard refinement

Topic matching alone could return irrelevant reference excerpts for unrelated
questions containing "hazard". Added finite source-lookup vocabulary; unknown
words and missing source-lookup intent refuse. Malicious question text refuses,
while malicious retrieved text remains an attributed inert quote. No semantic
model or unsafe fallback was introduced. Historical audit counts now reflect
the committed pair/referral message counts.

## P03-T02: Final implementation evidence

Final core selection: 108 passed; full project ruff/format/mypy passed (96 files).
Final agents selection: 45 passed; ruff found one long vocabulary literal,
corrected before Review; ruff/format/mypy then passed (19 files), seven focused
answer tests reran successfully including equality with the recorded evaluation.
Final API selection: 98 ran, 16 optional existing skips, no failures; full
ruff/format/mypy passed (45 files). Node syntax and git whitespace checks passed.
The loopback app is responsive and exercises the actual cited endpoints.

All P01-P03 source markers are complete. Eight acceptance rows are audited in
src/api/README.md with explicit partial/unmet operational gates; issue body is
unchanged. Per-project READMEs and append-only reference log updated. Commit/
push/PR delivery follows the requested one Review and is not an unchecked source
task. No source change remains planned before Review.
