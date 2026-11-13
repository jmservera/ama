---
title: Role-screen evidence parent integration plan (prospective)
description: Plan to merge two frozen children and append one qualified evidence record
ms.date: 2026-11-13
---

## Phases

1. Critique this plan with an independent agent before any merge (one pass, no repeat).
2. Merge `32fd2163` then `eeb8ec15` with `--no-ff` merge commits (noreply author plus Copilot trailer). No cherry-pick, no rewriting; original paths and bytes remain.
3. Append a compact dated section to `docs/architecture/cutover-evidence-pack.md`; add one link in `docs/reference/README.md`; append an entry to `docs/reference/log.md`.
4. Verify: blob-hash equality of every child path in the merge result, `src infra tools .github` equal to the base, `git diff --check`, ASCII scan of added lines, link review, secret scan of added public material.
5. Write the changes record, commit, freeze, and run one independent Review of the actual diff.

## Section content (boundaries)

Source pin, exact child heads, covered source-only versus locally observed assertions, original and recovery adverse verdicts, origin, resource and test coverage limits, unmet WCAG, human, AT and dependent gates. #149, #151, #231 and #232 stay open and unticked. Recommendation: continue safe existing demo lanes, not global acceptance. No requirement relaxation, new bug issue, business-policy decision, sensor checkpoint or approved sent-evidence contract.

## Stop conditions

A secret or private data in proposed public material stops the publication handoff without altering originals. Any file differing from its child blob stops the merge handoff.
