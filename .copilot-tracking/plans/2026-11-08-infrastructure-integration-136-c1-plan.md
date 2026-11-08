---
title: Infrastructure integration topic 136 corrective C1 plan
description: Plan for the docs-only corrective loop C1 on the issue 136 integration topic
ms.date: 2026-11-08
---

## Scope and tier

Task `infrastructure-integration-136-c1`, base HEAD `f28e1fe003e1e1d7d2fe43546cbbe0d4a92851d2`, `origin/main` `0f05e9aae70768def8d1d9c300215f9ee2f11638`. Local only; no push, PR, merge, issue write, tick, closing keyword or approval. Tier FOCUSED, documentation tracking records only. Validation is Markdown, link, Git diff and source blob review; no test, build, install, gate or service (owner CI-first direction, 08:15). Research: `.copilot-tracking/research/2026-11-08-infrastructure-integration-136-c1-research.md` (executed, Ready). Details: `.copilot-tracking/details/2026-11-08-infrastructure-integration-136-c1-details.md`.

## Steps

* [ ] 1 Currency: `git fetch origin main` before the amendment and before freeze; on drift report and stop, no merge or rebase.
* [ ] 2 Create one amendment record `.copilot-tracking/plans/2026-11-08-infrastructure-integration-136-c1-amendment.md` that supersedes, for current use only, original statements on F1, F2, F3. It carries the corrected 144 identity map, the corrected gate order with the src-ci path observation, and a complete one-row-per-file coverage table (9 top-level units, 20 modules) with path, wired-from, static status, owner and unknown or human approver.
* [ ] 3 Write a new current state `.copilot-tracking/rpi-sessions/2026-11-08/infrastructure-integration-136-c1-state.json` with the corrected follow-ups; leave the original state file as is.
* [ ] 4 Do not edit any original record or any non-tracking file. No rerun of the original critique.
* [ ] 5 Validation after the last write and again after the final commit: `git diff --check`, ASCII scan, closing-keyword scan, blob and path existence for every table row, scope check that the diff against `f28e1fe0` is added files only under `.copilot-tracking/`, with the single exception below.
* [ ] 6 Changes record, one author Review (execution separate from outcome, not independent assessment), commit. Plan step markers are the only edit to an existing file (this C1 plan); they mark this loop's own steps and never an issue criterion. The original records are not edited.
* [ ] 7 Freeze: ignored-inclusive clean, report HEAD, tree, current main, diff counts and remaining findings.

## Commit sequence

1. Research, plan, details, critique committed before the amendment exists.
2. Amendment and state.
3. Changes and Review with plan ticks. Identity from `gh api user` (id 8036360, login jmservera) as repository-local noreply for author and committer; Conventional messages, Copilot trailer, `Refs #136` only; no amend; explicit staging.

## Critique Disposition

One new independent critique of this corrective plan executed (verdict Revise, 3 blocking, 1 non-blocking), recorded in `.copilot-tracking/plans/2026-11-08-infrastructure-integration-136-c1-critique.md`; all applied (guard caller fix, marker wording, post-commit validation, full supersession inventory in research). It does not replace or rerun IC-001 to IC-005, whose IC-003 disposition is preserved as historical and corrected by the amendment.

## Follow-Up Items

* Coordinator: independent exact-head C1 assessment, then authorized push and draft parent PR; hosted checks selected by GitHub on the actual head before merge or any 144-dependent publication.
* 144: 107 and 118 source verification before engineering; session `0bd489d3-4546-4229-94f9-d1812eadef27` is a conversation identifier only.
* Owner: manual-row owners, Defender cost approval, issue and README refreshes.
