---
title: Issue 440 post-1500 checkpoint plan (0240)
description: Prospective plan for a docs-only provenance annex in the existing cutover evidence pack, Refs #440
ms.date: 2026-11-13
ms.topic: reference
---

## Status

Draft, prospective, local-only, not approved. Planned in this admission; implementation, Review and publication are separate later stages that need explicit root admission. Details: [details](../../details/2026-11-13/issue-440-post1500-0240-details.md). Research: [research](../../research/2026-11-13/issue-440-post1500-0240-research.md). Critique: [critique](./issue-440-post1500-0240-critique.md).

## Objective

Record one smallest post-1500 merged-main checkpoint as an appended annex in the existing `docs/architecture/cutover-evidence-pack.md`, reconciling the actual integrated wave with document-qualified requirements and ADR status, existing exact-input validation and provenance, failure, manual and approval boundaries and the remaining backlog. Separate four evidence classes: parent-source observations, fresh final C4 checks, hosted observations and actual merged-main provenance.

## Decision basis

Research found no genuinely missing focused observation (see research). The annex is documentation only. No source, test, workflow, manifest, infrastructure, README or acceptance change.

## Scope

In scope (implementation stage, later):

* One appended section in the pack, after the existing 149 checkpoint and its final evidence assembly, headed with the date and `Refs #440 #149 #96`, marked draft and not approved. Earlier sections stay byte-unchanged.
* Index and log hygiene required by the knowledge base conventions: an entry appended to `docs/reference/log.md` and the existing pack row in `docs/reference/README.md` only if its description materially changes (decide by reading the row; do not rewrite log history).
* Tracking records: this research, plan, details, critique, state; later changes and Review records under `.copilot-tracking`.

Out of scope: any correction cycle, #233, #203, #184, 135, 132, 144, 146, new issues, issue or board edits, acceptance ticks, #440 final two criteria, whole 149/A2/epic claims, pivots or deferrals, requirement relaxation.

## Phases

* P1 Re-pin. Fetch read-only; confirm main and tree still equal `ad1a17229`/`f650b1ba`; if main moved, re-evaluate which pinned facts changed, do not rebase or merge silently.
* P2 Draft annex with these subsections: trigger and identities; classes A to D with their qualifications; document status table (blobs equal to the existing section, no approval); updated traceability delta (only the WCAG baseline tied-field row, other rows unchanged by C4); hosted observations table (jobs, counts, skips, qualifications); what is superseded and what is preserved (core 72 historical reuse stays recorded, plus the hosted SQLite observation; SQL Server qualifications); failure, manual and approval boundaries; backlog and holds; recommendation CONTINUE bounded as a proposal; process limits.
* P3 Reconcile stale statements by appending, not rewriting: name each earlier sentence (no pull request, hosted unobserved, `test_live_doc_links` not run) and state its later disposition.
* P4 Focused checks the change itself touches: `git diff --check`, ASCII scan of added lines, no em dashes, relative-link review, and `test_live_doc_links` from `src/core` because it reads the pack. No other test, browser, SQL or gate run. State that none of these refreshes any wave count.
* P5 Independent Review once (genuine, after implementation), then independent exact-head assessment by root; hosted CI read for the exact head, with path-filtered or skipped workflows stated as not success.

## Fresh observation decision

None required. Evidence reuse rationale: C4 inputs have fresh covering results (13, 21, 4) and hosted `ok` lines on the merged tree; each parent lane stays input-equivalent only where its own named inputs are unchanged (product source bytes are unchanged, but C4 changed the baseline test and WCAG record, so the final API lint, format and type result is attributed to the fresh C4 canonical check, not the earlier types lane); hosted core, API, agents and SQL Server module runs on the merged tree supply wave-level observations with explicit qualifications. The one unresolved item (per-test SQL Server outcome and the single hosted skip) is recorded as a limit, with a conditional, not recommended, selector in the details.

## Validation tier and classification

Focused documentation tier: no workflow, gate-tool, dependency manifest, Dockerfile, permission, SQL schema, deployment or security-control change. A mixed change does not arise. A blanket `tools/rpi-checks.py --changed` run is optional and does not replace the planned direct checks; the complete gate and external receipt are not required. Review and exact-head assessment must reassess this classification; unresolved impact would take the full tier.

## Authority and dependencies

* Authority: root admission of the implementation stage by name, on a clean topic branch from current `origin/main`; no authority to approve a pivot, deferral or relaxation.
* Dependencies: #440 stays open; PR must use `Refs #440` (and `Refs` for others), never a closing keyword, empty closing references before and after, #83 verified open; independent exact-head review, human approval and owner merge decision; hosted CI for the exact head.
* Independent lanes unaffected: #203 held candidate (do not regenerate: its inputs overlap the pack), #184 held candidate, scoped 96 remaining allowance (untouched, no C5), #233 excluded, allowances for 135, 132, 184, 144, 146 not borrowed.

## Risks

* Overclaiming hosted success as acceptance: mitigated by explicit class separation and the not-established list.
* Mutable image tag and non-verbose SQL job: stated as limits.
* The annex edits a file that the 203 candidate and test_live_doc_links read: the link test is run once; 203 stays held.
* Pack size: append-only, one section, no archive reading.

## Next-stage resume conditions

Root admits Implement by name; the worktree is clean at the committed planning candidate; `origin/main` is re-fetched and either unchanged or its movement is assessed; the critique dispositions are honoured; the stated stop rules hold (no fresh-count campaigns, no correction cycle). Review executes once; findings route to later work.

## Critique disposition

Recorded in the critique file; compatible findings applied directly in this plan and details.
