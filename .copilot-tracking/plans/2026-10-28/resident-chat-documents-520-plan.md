---
title: Resident chat document correction plan
description: Bounded own-case requests, presented documents and issue explanations
ms.date: 2026-10-28
---

## Task Metadata

* Task ID: 520-documents-correction
* Task slug: resident-chat-documents-520
* Planning status: Ready; original critique Revise, all three findings directly resolved
* Details: .copilot-tracking/details/2026-10-28/resident-chat-documents-520-phase-details.md
* Critique: .copilot-tracking/reviews/plans/2026-10-28/resident-chat-documents-520-plan-critique.md

## Executive Summary

Extend the existing own-case SQL projection and mandatory rules answer with
resident-facing document requests, instructions and recorded issues. Keep AI
limited to selecting existing guidance; the facts and citations remain host-owned.

### What You May Not Know

The staff evidence checklist is not a request to a resident. Missing request data
must remain unknown. A stored or scan-clean file does not establish acceptance.
The source view must be separately applied before a deployed service can use new
columns; this cycle performs no Azure work.

## User Decisions and Requirements

* Complete research, plan, implement and independent review for PR #525 / #520.
* Use src, synthetic own-record data, citations, identical AI-off rules facts,
  plain wording and staff referral without acceptable/compliant claims.
* Add focused tests and extend the actual browser check.
* Never read .env/private datasets or use Azure/secrets. Ruff length remains 100.
* Commit dated evidence with resolved GitHub noreply identity and required trailer,
  rebase remote topic branch, locked nonblocking full gate, normal push.
* Do not use PR closing keywords while any issue criterion remains unproven.

## Goals

* Close the missing document-answer behavior without enlarging model authority.

## Scope and Non-Goals

Include core parsing/explanation, view/reader/HTTP wiring, tests, browser check and
direct component documentation. Exclude upload UI, byte inspection, live services,
legal decisions, staff payload reuse, design changes and whole-issue approval.

## Functional Requirements

* Case JSON `resident_document_requests`: null/absent means unknown; a list contains
  unique `{id, kind, how_to_provide}` resident-facing entries.
* Canonical `documents` project only id, kind, generated, scan.status and explicitly
  resident-facing `resident_issues` (`severity`: warning/error, `message`: plain text).
  Never expose filenames, bytes, staff notes, scanner detail or arbitrary case fields.
* Match requests to nongenerated presented documents by recorded kind. Report
  no presented document, not a legal deficiency; received does not mean accepted.
* Explain every recorded resident-facing issue and known scan issue. Unknown scan
  or issue data stays explicit. Instructions come only from the own-case request;
  otherwise ask staff for a secure provision route; no upload in chat.
* Include stable request/document references in sources. Preserve consent, fresh
  auth/revocation and no user-selected case. Typed document questions, including
  "how to provide/send", must route to documents without authorizing sending.

## Non-Functional Requirements

* Strict bounded shapes: at most 20 requests, 40 documents, 10 issues/document,
  64-character IDs, 80-character kinds, 500-character instructions/issue messages.
  Malformed/oversized data fails closed explicitly, never truncates facts.
* No model prose or interpretation; same deterministic base under success/fallback.
* Preserve 100-column Ruff, typing, existing presentation and human acceptance gates.

## Acceptance Criteria

* Constructed cases prove missing/provision/warning/error facts and per-item citations,
  empty vs unknown data, pending/unknown/clean scan boundaries, generated placeholders,
  multiple documents, malformed/oversized shapes, and another resident's non-disclosure.
* AI selection and unavailable fallback preserve the exact rules facts and sources.
* Actual browser checks typed/selected document questions, rendered citations/issues,
  cross-session isolation and long document answer reflow with existing axe checks.
* SQL integration proves named projection and no private fields, own-case filtering
  and existing view-only grants using disposable local SQL.
* SQL preserves invalidity before lossy extraction: source-through-view tests cover
  absent/null/empty and wrong-type containers, numeric text, oversized text/lists.
  Valid boundary values remain unchanged; invalid markers cause explicit denial.
* All scan codes clean/pending/infected/mismatch and unknown are distinct; clean
  never approves content. Synthetic infected/mismatch rows do not imply normal
  upload persistence: upload rejects and rescan normally removes such files.
* Independent critique/Review preserved; full exact-head local gate passes under
  `/tmp/ama-rpi-heavy.lock` with `--lock-timeout 0` before publication.

## Sources

Research: .copilot-tracking/research/2026-10-28/resident-chat-documents-520-research.md,
C1-C6 and W1. Original first-pass artifacts are unchanged.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Own-case document contract and answer

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Implement projection, parser and bounded advisor wiring

Targets: core resident documents helper, resident showcase/SQL/assistant, SQL view,
API app/router. Details own schema and negative cases.

<!-- rpi:phase id=P02 -->
### [x] P02: Focused evidence and documentation

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Add semantic regressions and browser assertions

Test ownership: core owns parsing/explanation and SQL; API owns HTTP/advisor/browser.
No test removals. Maximum additions: two test files and 24 test methods.
Canonical targets are src code, infra SQL and component README. No generated source.
Semantic coverage proves new facts; regression coverage preserves auth and fallback.

<!-- rpi:phase id=P03 -->
### [ ] P03: Review and publication

<!-- rpi:task id=P03-T01 -->
#### [ ] P03-T01: Preserve independent Review, commit, rebase, gate and push

Commit implementation and dated original evidence; rebase only the explicitly
authorized remote branch, never force-push. Run full gate on final clean candidate,
fetch main, verify receipt and independently assess exact head before normal push.
If lock busy or gate fails, record blocked publication without weakening checks.

## Dependencies

* Existing SQL view-only reader and bounded advisor contracts.
* Local installed distributions/tools; current shell lacks zava_forward, so restore
  existing pinned dev dependencies in an external venv before focused tests.

## Critique Disposition

One independent critique executed, verdict Revise (original preserved).
PC-001 resolved directly: source-through-real-SQL validity and boundary proof is
now explicit above and in P01/P02 details. PC-002 resolved directly: all four scan
codes plus unknown are explicitly mapped/tested with no acceptance inference.
PC-003 resolved directly: P03 details pin reviewed origin/main and exact --base
arguments, with moved-main stop/rerun. Owner: planning parent for all dispositions;
none requires a divergent user decision. No second critique.

## Follow-Up Items

* Human/resident/assistive-technology and real-model acceptance remain pending from
  the original task; this correction does not establish whole-issue acceptance.

## Handoff

Implementation changes record:
.copilot-tracking/changes/2026-10-28/resident-chat-documents-520-changes.md.
P01/P02 implemented and locally validated; ready for original independent Review.
P03 publication remains pending the committed exact-head full gate; no full-plan
completion or human acceptance is claimed.
