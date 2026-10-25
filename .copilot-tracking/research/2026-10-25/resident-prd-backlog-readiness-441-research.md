---
title: Resident PRD and backlog readiness research (issue 441)
description: Evidence for owner-decision corrections and a draft resident backlog, documentation only
ms.date: 2026-10-25
---

## Brief and opening state

Task jmservera/ama#441 (OPEN), slug resident-prd-backlog-readiness-441, branch
docs/resident-prd-backlog-readiness-441 from origin/main 5d79aaee (verified
after fetch). PR 442 merged; its branch is not reused. Documentation and draft
backlog only. Research disposition: executed (read-only; no application, cloud
or heavy-gate action).

Questions: current versions and registries; which owner answers conflict with
current text; overlap with PRs 424, 426, 439 and issue 444; what first-milestone
and sizing evidence exists; which findings remain open.

## Evidence

* Versions (verified): BRD v0.21.0 draft (FR-053 to FR-062, AC-104 to AC-126
  resident; FR-063/064, AC-127 to AC-132 staff access); PRD v0.20.0 at start
  (resident FR-062 to FR-071, AC-111 to AC-140; staff FR-072/073, AC-141 to
  AC-147; NFR-018 to NFR-021). Separate namespaces; no renumbering needed.
  Proposal: id null, unregistered, status proposed. Numbered ADRs 0001 to 0006.
* Owner decisions: comment 6389938010 and follow-up 6391945752 (see task).
* PRD already proposed p95 <=2s/five sessions/30 min (NFR-021, AC-139) and
  10 MiB uploads as author-proposed. Conflict: NFR-002 core acceptance states
  list/detail p95 <=1s and 5 MB/file with 100 MB total; the proposal recorded
  "precedence debt" pr442-qual-041 (both unresolved). The owner answers
  resolve scope: resident-specific targets, staff/core preserved, shared
  applicability explicit. BRD has no resident latency or size target, so the BRD
  needs no change; OD-55 wording stays.
* Identity: PRD S01 required an "approved synthetic identity configuration";
  the owner selected provider-neutral synthetic fixtures with no provider. OQ-030
  stays open for real accounts.
* Stories/stages: twenty stories S01 to S20, R0 to R5, six journeys with 30
  criteria exist; they are refined, not duplicated. M1 maps to R0 plus S01 to S06.
* Existing coverage: issue 444 (read-only loopback synthetic preview; local
  branch a3e527fd, 24 files, unpushed; excludes uploads and downloads).
* Overlap (open PRs, non-tracking paths): 424 head a74652aa (docs/reference
  README and log, form-review pack, src/core README); 426 head 419857b4
  (README, log, ADR 0002, ux research, src/api README); 439 head 3648875e
  (addendum, README, log); 444 local worktree (README, log, src/api and src/core
  README plus code). Shared with this slice: docs/reference/README.md and
  log.md (append-only/new rows) and, for 439, the addendum. No PR touches the
  PRD, BRD, proposal or residents.md. Strategy: minimal edits, rebase and
  reconcile both lanes at merge; recheck heads before publication.
* Open findings preserved: pr442-qual-005, 040, 006, 024, 041, 009, 039
  (see correction3 review RV-002); OD-52 to OD-55; registration UNMET; A5/B6
  hosted findings.
* No sizing evidence exists (no velocity, no estimates); no date is derivable.

## Planning readiness

Ready. Selected approach: in-place PRD correction (NFR-021, AC-139, new
applicability and sequencing subsections, S01 dependency, OQ-030/031, history,
version 0.21.0), aligned proposal and coupled addendum/journey/index notices, a
reviewable draft backlog, append-only log. Rejected: BRD edit (no
contradiction), new IDs, ADR registration, issue creation.
