<!-- markdownlint-disable-file -->
---
title: Issue 349 PR437 current scope reconciliation plan
description: Current prospective coordinator decision amending the original file-ownership boundary for the runner correction
ms.date: 2026-10-26
---

Written 2026-10-26 (after the 09:41 UTC coordinator handoff), before this amendment's critique and before
any further artifact edit. It is a current decision; it does not claim that these
decisions or a critique existed earlier. Original plans, text and chronology are
unchanged. Source and tests remain byte-identical to 1da56057.

## Coordinator decisions recorded (source: coordinator handoff 2026-10-26 09:41 UTC)

* RV-001: the original 2026-10-22 plan's strict file ownership (no edits to
  tools/rpi-checks.py) is superseded ONLY for tools/rpi-checks.py and
  tools/test_rpi_checks.py, ONLY for the reviewed image_build_argv and
  --no-cache correction of the four scanned images. No workflow, Dockerfile,
  scanner, ignore, threshold or dependency change is authorised. It is
  engineering for the observed stale apt-upgrade cache, not Entra, tenant or
  cloud authority.
* RV-005: merge 147980af message-only amend (identical trees to 211d048e) and
  the nohup launch of the final gate are recorded nonconformances, not
  retroactively authorised or approved, not waived or accepted by the owner. No
  repeat. For the technical partial-delivery gate they are disclosed process
  residuals. No higher-priority owner instruction requiring retrospective waiver
  was found by me; none is inferred.
* RV-002 stays an owner criteria follow-up: #349 open, Refs only, no ticks.
* RV-003, RV-004: summaries and stale markers stay disclosed, no fabrication.
  Current markers are reconciled by factual retrospective status only.
* RV-006: patch archive bytes preserved.

## Phases

* [x] Phase 1: this plan, written before critique.
* [x] Phase 2: one independent critique executed (rubber-duck, Revise; blocking: impossible future timestamp, corrected; two non-blocking items applied below). Return preserved in reviews/plans/2026-10-26/issue349-pr-scope-reconciliation-plan-critique.md. No repeat.
* [ ] Phase 3: changes record and a dated current-disposition section appended to
  the single technical-readiness review record; original verdict and findings
  kept as dated history. No other existing file edited. Acceptance conditions (critique PC-002, PC-003): the addendum retains the original conclusion that a technical partial merge recommendation is not yet supportable, lists the open prerequisites (RV-005 disposition status, hosted exact-head CI at the new head, coordinator assessment), and states that receipt e35fecc0 validates only 1da56057, is historical for the new head and is not whole-issue acceptance.
* [ ] Phase 4: validate tracking-only diff, commit, no push.

## Current retrospective marker status (factual, not original relabelling)

* image-no-cache-correction2 plan phases 2 to 5 were executed per its changes
  record and review; the plan file's markers stay as originally written.
* main-acafc6ee integration had no critique or independent review; coverage is
  limited to the clean automatic merge evidence, the coordinator assessment and
  the passed full gate on 1da56057.

## Constraints

No source, test, workflow, Dockerfile or scanner edit; no amend, rebase or push;
no gate; the e35fecc0 receipt becomes historical for the new head (artifact-only
commit); no receipt-recording commit.
