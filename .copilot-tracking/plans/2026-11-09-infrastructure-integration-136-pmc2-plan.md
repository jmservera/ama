---
title: Infrastructure integration 136 metadata correction C2 plan
description: Prospective plan for two docs-only metadata corrections to the 136 post-merge records
ms.date: 2026-11-09
---

## Provenance

Written and committed before any correction edit, after the C2 research. Details: `.copilot-tracking/details/2026-11-09-infrastructure-integration-136-pmc2-details.md`. Author: native rpi-agent (Claude Sonnet 5.5). The independent critique agent is a separate role and is attributed in the Critique result.

## Plan

* P1 Commit research, plan and details; run one independent critique of this plan and record its disposition before any edit.
* P2 Re-fetch `origin/main`. If it is no longer `1f28d09130c8e058a0436d468e6a22f3c4c24f47`, reclassify the overlap before editing; do not merge or rebase.
* P3 Correct the PM state JSON `next_action` to the ordered sequence: independent exact-head and current-base assessment (the same independent reviewer closes the exact correction delta; escalate if unavailable), then separately authorized forward PR-head publication or update (no force push, no rebase), then the actual new-head hosted checks GitHub selects and branch protection requires (a legitimately unselected or path-filtered workflow is neither a failure nor a success), then gated merge. State that checks on the unpublished head are not required and old remote `f16a398d4` has no check evidence and cannot validate the candidate. Add a `confirmed_decisions` entry recording the C2 supersession date and basis.
* P4 Append a dated correction section to the PM plan's Critique result attributing the independent critique to the host-displayed `gpt-6.1-terra` rubber-duck, distinguishing the author (Claude Sonnet 5.5). Leave the original sentence, verdict and findings text unchanged so history stays visible; the correction supersedes the model attribution only.
* P5 Add C2 changes, review and state records. Do not edit original reviews, critiques or commits. No checkbox is ticked.
* P6 Checks (docs-only, no local gate): `python3 -m json.tool` on changed JSON, relative-link and path-existence review of new records, `git diff` inventory showing only `.copilot-tracking/` paths, confirmation that non-tracking tree is unchanged from the start.
* P7 No push, PR, issue, board or merge. `Refs #136` only; all five epic criteria remain unproven.

## Critique

One independent critique of this prospective plan runs before implementation; it is recorded below and is not repeated.

## Success

Clean frozen local head one or more commits above `fc6adc5c5`; two defects corrected with original text preserved; non-tracking tree identical to `fc6adc5c5`; no 136 criterion claimed.

## Critique result

Executed once by an independent read-only rubber-duck agent on HEAD `f4be0e417` (the host-displayed model is in the native stdout log, not asserted here). Verdict: proceed with changes. All findings are accepted as direct corrections; no user decision is needed:

* PC-001 (blocking) the corrected sequence must retain the requirement that the same independent reviewer closes the exact correction delta, escalating if that reviewer is unavailable. Applied to P3 and details.
* PC-002 "actual new-head hosted checks" means the checks GitHub selects and branch protection requires for the new head; a legitimately path-filtered or unselected workflow is not a failure and not a success. Applied to P3.
* PC-003 the hosted evidence claim is bounded to the observed head and retrieval time (`f16a398d4`, empty rollup, 2026-11-09), not to every historical head. Applied to the research.

The critique is not repeated.
