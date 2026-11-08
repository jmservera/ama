---
title: AI and employee chat main stabilization 440 correction1 plan
ms.date: 2026-11-08
---

## Plan

Corrective docs-only iteration for assessment `review-440-c96a` on candidate `c96a3231`. Research: `.copilot-tracking/research/2026-11-08-ai-main-stabilization-440-correction1-research.md`. Details: `.copilot-tracking/details/2026-11-08-ai-main-stabilization-440-correction1-details.md`. Original c96a records are not edited.

* [x] Phase 1: Edit the c96a pack section in `docs/architecture/cutover-evidence-pack.md` only (finding F1 AWF recovery vs remediation; F2 current identities and pin-scoped exclusions; F4 review row; F5 F1 disposition wording). Add one dated "Correction 1 and currency" subsection and keep the earlier text as source-qualified history rather than silently rewriting it, except where the row is itself the incorrect statement (rows are corrected in place with the correction recorded).
* [x] Phase 2: Add the amended-reading statement (F3) to the same subsection, pointing at the new research record. Do not edit the original research file.
* [x] Phase 3: Update the index paragraph in `docs/reference/README.md` for currency and append a dated currency and correction entry to `docs/reference/log.md` (append-only, earlier entries unchanged).
* [x] Phase 4: Validation: `git diff --check`, ASCII and no-em-dash check on added lines, anchor and relative-link resolution, scope guard (only the three docs files plus `.copilot-tracking`), source-identity proof (existing hashes, no source diff to the audited modules), no rerun of unchanged suites. Re-fetch `origin/main` and record any further movement.
* [x] Phase 5: Changes record, one author Review, state, identity, commit with trailer, clean frozen candidate.

## Scope and constraints

* No application, tool, test, workflow, agent, BRD, PRD, ADR or decision change. No push, PR, merge, issue or board writes, ticks, policy activation, deferral or approval, Azure or model action, cleanup, broad tests, new services, force or rebase. Parent PR 1240 and its worktree are not touched.
* Original adverse claims in c96a records and in the pack stay visible. Corrections add dated qualification and mark which earlier statement they supersede.
* No old observation becomes fresh acceptance. Skipped SQL and browser checks stay unverified.

## Acceptance for the iteration

* F1: no statement says AWF 504 is a current failure or Blocked. History is dated and source-qualified (run `42472167065`, #1275 head `4db31928`, 2026-11-08T10:38Z rootless checksums-and-bundle install passed); recovery and remediation are distinguished; #1274 stays open.
* F2: pinned 608c observation retained; current identities `main` `3c57a02d` / tree `3ed3dec0`, #1278 as `e73d4210` / `feff48a4` on main, #1243 as `6ef6dc36` / `0006f193` on the parent branch, PR 1240 open at head `6ef6dc36`; exclusions scoped to the 608c pin.
* F3: unsupported reading claim amended in new evidence; mandated inputs read with honest ranges.
* F4: Assistants.review row states what source enforces and that general requester separation is not enforced.
* F5: F1 is unowned, unfiled, pending triage as a proposed refactor, not a deferral.
