---
title: Issue 83 table inventory D1 plan
ms.date: 2026-11-11
task_id: issue-83-table-inventory-d1-1111
parent_task: issue-83-waiting-view-1111
---

## Objective

Register the audited thirteenth script-built table (the #83 waiting table) in the existing WCAG table inventory check and record, to clear hosted failure `test_every_table_has_a_caption_and_column_headers` (13 != 12). Test and documentation metadata only. Research: `.copilot-tracking/research/2026-11-11-issue-83-table-inventory-d1-1111-research.md`.

## Boundaries

* Product files stay byte-identical to dd3c32910c3c5205a2cbedbe74608411c6f9f341: everything under `src/api/src`, `src/core`, `src/agents`, API, CSS, store, permissions. Proof: `git diff --stat dd3c32910 -- src ':!src/api/tests'` empty.
* Preserve regex, site enumeration, caption check, bare-`th` ban and count-fail mechanism. Literal 13, no lower bound, no dynamic expected value.
* No new regression unless it guards something the mechanism does not (decision in research: none).
* Stop and report if audit shows a real product accessibility defect. No D2. No push, PR, issue or board change.
* Out of scope: original critique's three Low relative links, unbounded-row performance qualification, `ops.js` line 28 form.

## Phases

* [x] P01 Pre-change reproduction retained and table audit confirmed (research C1 to C5)
* [x] P02 Update `src/api/tests/test_accessibility_baseline.py` count 12 to 13 with the comment naming the waiting table and the record
* [x] P03 Update the baseline Tables row (and G-4 context if needed), `docs/reference/README.md` entry and append `docs/reference/log.md` entry
* [x] P04 Focused validation and product byte-equality proof
* [x] P05 Original D1 Review
* [x] P06 Local identity, one Conventional Commit, clean tree and byte-equality proof on the committed head

## Validation

From `src/api` with PYTHONPATH on the worktree sources: the single failing test then the whole `test_accessibility_baseline`; with `ZF_BROWSER_TESTS=1`: `test_handoff_waiting_view`, `test_unaccepted_handoff_download_ui`, `test_handoff_read_guidance`, `test_handoff_api`, `test_role_endpoint_inventory`, `test_workbench`, `test_role_screens` (expect 69 selected tests, zero skips); `node --check` app.js; ruff check and format check and mypy on the changed test. No full gate, SQL, image, cloud or AT.

## Follow-Up Items

* OD-09 approved times and operational acceptance (human). Whole #83 criterion 3 unmet.
* Screen-reader, reflow and manual conformance checks for the waiting table remain unperformed.

## Critique Disposition

One critique (Revise; 0 Critical/High, 3 Medium, 3 Low), applied directly; no repeat, no user decision. Critique: `.copilot-tracking/plans/2026-11-11-issue-83-table-inventory-d1-1111-plan-critique.md`.

| Finding | Disposition |
| --- | --- |
| PC-004 | Accepted. Add phase P06: set local privacy-safe noreply identity (author and committer), one Conventional Commit with Co-authored-by trailer, then prove byte equality against dd3c32910 on the committed head and clean tree. |
| PC-001 | Accepted. The record states 13 is the regex-counted set and names `ops.js` line 28 (`aria-label`, no caption) as an uncounted, unaudited-by-this-test form outside this D1. |
| PC-005 | Accepted. Local pass is not a hosted pass; the hosted job for the new head stays unobserved and is reported so. |
| PC-002 | Accepted. Leave G-4 unchanged (its general wording stays true); set the baseline frontmatter `ms.date` to 2026-11-11 for the material edit. |
| PC-003 | Accepted. Log heading `## [2026-11-11] update | WCAG table inventory registers the handoff waiting table (Refs #83)`, evidence class: source audit plus constructed browser tests, no AT, no conformance, no criterion tick, no approval. |
| PC-006 | Accepted. The 69 figure is the coordinator's instruction, not a verified count; report the actual count and skips. |

