---
title: Infrastructure integration 136 post-merge refresh plan
description: Prospective plan to merge current main into the 136 recovery branch and refresh evidence only
ms.date: 2026-11-09
---

## Provenance

Written and committed before the merge, after the post-merge research. Details: `.copilot-tracking/details/2026-11-09-infrastructure-integration-136-pm-details.md`.

## Plan

* P1 Commit the research, this plan and details; then run one critique (below) and record its disposition before any merge.
* P2 Re-fetch and confirm `origin/main` is still `d4d6827fe60be651cd922ab9656688c18c978e1d`; if it moved, stop and reassess scope, merge base and conflicts against the newly pinned commit before merging. Record the pre-merge HEAD (the commit of this plan's critique record). Run `git merge --no-ff origin/main` normally into the same branch with a Conventional Commit message and the Copilot trailer. No rebase, reset, force push, retarget or squash.
* P3 If a conflict arises, resolve by keeping both intents; if intent cannot be reconciled, stop and record the exact blocker.
* P4 Verify the preserved evidence: every path under `.copilot-tracking/` that exists at `24d1cfb16` is byte-identical (same blob ids) in the merge result, covering the original 16 records, R1/R1C1 records, earlier critiques and Reviews. External evidence (independent-136-c1 reports, handoff-136-c1.md) is outside the repository and is not modified. The branch adds no `docs/reference/log.md` entry (it has no diff against the merge base); the check is that the merged `docs/reference/log.md` is byte-identical to `origin/main`'s, so main's append-only entries are preserved in full.
* P5 Demonstrate that source, tests, dependency manifests and infra are unchanged relative to the approved candidate except for the main delta: compare tree ids of the non-tracking content (`git ls-tree -r` including modes, excluding `.copilot-tracking/`) of the merge result and `origin/main`; they must be identical, and the approved candidate's non-tracking tree must equal the merge base's.
* P6 Add changes, review and state records, then commit. Write the handoff in the coordinator session files directory.
* P7 Validation tier: pure documentation, owner demo tier, no local gate, no tests, services or deployment. Checks: relative-link existence in the new records, Markdown review, scoped diff inventory.
* P8 No push, PR, board or issue writes. Use `Refs #136` only; all five criteria stay open.

## Critique

One independent critique of this prospective plan runs before implementation; it is recorded in the Critique result section below and is not repeated.

## Success

Clean frozen local head; the merge commit's parents are the recorded pre-merge HEAD (descending from `24d1cfb16`) and `d4d6827fe`; P5 equality holds; no 136 criterion is claimed.

## Critique result

Executed once by an independent read-only rubber-duck agent (claude-sonnet-5.5 harness default) on HEAD `008a8dea2`. Verdict: proceed with changes. Findings, all accepted as direct corrections with no user decision needed:

* PC-001 the first merge parent is the recorded pre-merge HEAD, not `24d1cfb16`. Applied in P2 and Success.
* PC-002 P5 compared filenames only. Replaced by a tree-id comparison including modes. Applied in P5.
* PC-003 preservation needs byte identity, and the log claim needed identification. Applied in P4; the branch has no log.md diff, so the earlier "both log entries" wording is read as main's append-only log being preserved in full.
* PC-004 a moved main requires stop and reassessment. Applied in P2.

The critique is not repeated.

### Correction C2 (2026-11-09)

The sentence above, which names `claude-sonnet-5.5 harness default` for the critique agent, is superseded for attribution only. The native stdout of the post-merge refresh run (coordinator session log `rpi-136-postmerge-refresh.log`, line 76) displays `Rubber-duck (model: gpt-6.1-terra) Critique post-merge plan` with verdict `proceed with changes`. The independent critique was therefore executed by the gpt-6.1-terra rubber-duck agent. Claude Sonnet 5.5 is the author of the plan and of the native rpi-agent run, a separate role. The verdict, PC-001 to PC-004 and the original commits `008a8dea2` and `b1cf9b525` are unchanged and not regraded. See `.copilot-tracking/changes/2026-11-09-infrastructure-integration-136-pmc2-changes.md`.
