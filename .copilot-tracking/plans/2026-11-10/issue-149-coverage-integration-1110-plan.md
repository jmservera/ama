---
title: Issue 149 coverage parent integration plan
description: Prospective plan to merge current main into the reviewed parent 149 topic, qualify the combined source with focused checks and record a dated stabilization section
ms.date: 2026-11-10
---

## Task and boundaries

* Task `issue-149-coverage-integration-1110`, research [research](../../research/2026-11-10/issue-149-coverage-integration-1110-research.md), details [details](../../details/2026-11-10/issue-149-coverage-integration-1110-details.md), critique [critique](../../reviews/2026-11-10/issue-149-coverage-integration-1110-critique.md).
* Input parent `ae4b20007ec9bc1d4bd5dd3eef91445f29f5e50f`, main `d52f20a5198de7269f39daf794911545aee01ced`, prospective clean merge tree `a9b51381c57eb233e8aae2371a3b8456e23147ab`.
* Allowed: normal merge, minimal conflict reconciliation preserving both sides, the dated cutover-pack section, necessary existing index and log links, own RPI evidence. Not allowed: new behavior, threshold, role, consent, approval, model, infrastructure or schema change, #156 M1 decision, #1362 or #1371 fix, #80 or #216 source, push, PR, GitHub edit, merge to main.
* A real defect or unrelated correction stops the candidate and is routed to Root, not repaired.

## Phases

* [x] P1 Merge. Confirm clean tree and tracked-state; `git fetch`; if main moved, record and stop for Root; otherwise `git merge --no-ff origin/main` with the repository-local identity and the Copilot trailer. Verify the merge tree equals the prospective tree `a9b51381` and that there are no conflict markers.
* [x] P2 Qualify the combined source with the focused set listed in the details: installs, focused API, Core and importer unit, configured ruff and file-less mypy, nonqueued Chromium harnesses, web-guideline read, #1362 handoff read.
* [x] P3 Record. Add one dated section at the end of `docs/architecture/cutover-evidence-pack.md` (identities, observed commands, classification, trace, findings, owners, gates, recommendation). Add one row to `docs/reference/README.md` only if the index lists the pack's checkpoint sections, and one append-only entry to `docs/reference/log.md`.
* [x] P4 Reconcile changes record, state and plan markers, link and ASCII check, `git diff` review, commit the tracking and documentation as a second normal commit with the Copilot trailer.
* [ ] P5 Single Review of the final boundary, then freeze the clean local candidate.

## Success criteria

* Combined tree has both sides' content and append-only entries (docs README and log from both histories present once).
* Every selected check exits 0, or a failure is preserved with its exact reproduction and publication is marked blocked. No retry-until-green.
* The cutover section separates current merged-main evidence from parent-only integration, approved from draft or proposed requirements, and local observed from implemented-unverified, blocked, deferred and unknown. It uses `Refs #149 #440` and covered children only, no closing keyword, no criterion tick.
* Whole UX, WCAG, assistive-technology, human, content and design acceptance remains unmet and stated.

## Gates

Critique: one pass on the final candidate plan, recorded before plan-done. Review: one pass after implement-done. Hosted CI, independent exact-head assessment and human approval remain outstanding and are not claimed.
