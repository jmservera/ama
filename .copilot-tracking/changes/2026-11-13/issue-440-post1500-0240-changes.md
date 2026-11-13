---
title: Issue 440 post-1500 implementation changes (0240)
description: Changes record for the docs-only post-1500 provenance annex
ms.date: 2026-11-13
ms.topic: reference
---

## Changes

* `docs/architecture/cutover-evidence-pack.md`: appended one section, "Post-1500 merged-main provenance checkpoint (2026-11-13, Refs #440 #149 #96)" (63 added lines, none removed).
* `docs/reference/log.md`: appended one entry (6 added lines, none removed).
* `.copilot-tracking/plans/2026-11-13/issue-440-post1500-0240-admission.md`: root admission and the four clarifications A1 to A4, written before the canonical edits.
* Index (`docs/reference/README.md`): no change. The pack's index description is not materially changed and the previous 149 checkpoint section is not indexed either.

## Amendments and divergences

* Clarifications A1 to A4 applied as admitted. The annex keeps core 72 as historical reuse, makes no 72-wide claim and does not identify the SQL Server twin outcome.
* Correction to the planning research: the SQL Server twin of the funding-membership test was observed skipped in the src-api job, not src-core. The research file is unrewritten; the admission and annex state the correct job.
* The annex uses the existing PRD "Accessibility engineering" row (NFR-001 and NFR-012, AC-034 and AC-037), labelled not owner-confirmed, instead of the planning text's "nearest" mapping.
* Push scorer `43353567759`: in_progress, no conclusion at read; recorded as pending.

## Checks run (documentation only)

* `git diff --check`: clean. ASCII and em dash scan of added lines: none found. No removed lines. Link review: one new relative link (log to the pack anchor), the `test_live_doc_links` module resolves it.
* From `src/core`: `python3 -m unittest tests.test_live_doc_links`: 2 tests OK with the existing environment. Direct check of a changed input, not a wave count refresh.
* Not run: browser, SQL, Docker, scanner, model, provider, Azure, whole suites, `--changed` and complete gate. Focused documentation tier: no workflow, gate-tool, manifest, Dockerfile, permission, SQL, deployment or security-control change.
* Hosted evidence re-read read-only: Source CI run `43351173623` counts and named lines, scorer `43351173644` (pull_request, completed success), push scorer `43353567759`. No raw log copied; the temporary log was removed.

## Reading limits

Original case study read in full; the addendum read only in its Purpose and Status section (158 KB); owner memory read as context and not cited; the index read by pack row and last checkpoint paragraphs, not end to end. No source, test, workflow, infrastructure or manifest file changed; `src` tree equals main.
