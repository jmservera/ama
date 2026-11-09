---
title: Infrastructure integration 136 recovery correction R1C1 plan
description: Prospective plan for three bounded corrections of the R1 recovery records
ms.date: 2026-11-09
---

## Provenance

This plan is written and committed before any implementation edit, as its own commit after the R1C1 research. It follows the R1C1 research in the same session. No retrospective statement is made.

## Plan

* P1 Add `plans/2026-11-09-infrastructure-integration-136-r1c1-amendment.md` as the superseding record for R1 provenance, the five-criterion matrix and six-file accounting. Link, do not copy, the original matrix.
* P2 Add short qualifier lines in the R1 plan, review and changes records (current use only): R1 was recorded in one operation, the scope assessment was author-inline, the review lists all five unproven criteria, and R1 adds six files. Original wording stays as history.
* P3 Replace the R1 plan success wording that mixes "six artifacts plus state" by the qualifier, not by rewriting the original sentence.
* P4 Add R1C1 changes, review and state. Write `handoff-136-c1.md` in the coordinator session files directory with corrected accounting.
* P5 Do not edit the original 16 files, native logs, earlier critiques or reviews, Bicep, source, KB, issues or PRs. No push.
* P6 Validation tier: pure documentation, owner demo tier, no local gate, no tests, services or deployment. Check: original 16 byte equality with the frozen HEAD, tracking-only diff, link existence, file counts.
* P7 Commit locally with repository-local identity `8036360+jmservera@users.noreply.github.com` and the Copilot trailer.

## Critique

One author-inline scope assessment is performed when this plan is written: scope is three corrections, no conflict with confirmed decisions, no independent critique is claimed. A later independent exact-head review by the coordinator is the independent control. It is not repeated.

## Success

`git diff --name-only origin/main...HEAD` outside `.copilot-tracking/` is empty. Expected diff: 22 plus R1C1 additions (research, plan, details, amendment, changes, review as Markdown, plus state JSON; seven added files). All five #136 criteria stay unproven.
