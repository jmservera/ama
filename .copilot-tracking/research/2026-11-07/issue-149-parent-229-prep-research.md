---
title: Issue 149 parent preparation for child 229 browser regression, research
ms.date: 2026-11-07
---

## Research

* Original session: 978d4601-9d13-4110-ac90-aea0eac18f18 (issue 149, resumed). Disposition: executed (read-only git, issue and review inspection).
* Scope: prepare the existing parent topic `test/ux-evidence-149` for one independent child 229 maintained browser regression of the employee AI exception register already on main (PRs 1257 and 1260). Not new product, recovery or AI authority; not UX, WCAG, assistive-technology, usability or epic 149 acceptance. Issue 149 and 229 criteria are unchanged: 149 all open; 229 has only the WCAG 2.2 criterion unticked.
* Pinned state: local HEAD bb3a3b03 (clean, no ignored files); upstream dbeab436 (fast-forward descendant of HEAD, adds #1237 c66f2cdd and #1224 233 tensions); main f0afa8d7, merge base with parent bb3a3b03.
* Parent delta over bb3a3b03 (52 files, +1606/-10): `src/api/checks/atlas_tensions_browser_check.py`, `test_atlas_tensions_checker.py`, test edits (content standard, document controls, role screens conformance), UX docs, README, log, RPI artifacts, and `doc_controls.py` refusal wording only (reason, owner, next action; legal-hold and retention predicates, audit events and deletion behaviour unchanged, per original 153 review and coordinator independent review 2026-11-06).
* Why adoption of main is needed: `src/web/role-screens.js` on main (blob 55f503...) carries the newer exception register UI; the parent copy differs. `data_operator_browser_check.py` is byte-identical between parent and main (blob f7529d8d). A child started from stale parent would test stale UI.
* Dry-run merge trees (read-only `git merge-tree`): bb3a..dbeab436 clean; dbeab436 + main clean. No conflicts expected; the main-relative parent delta must equal the 233/153 source delta.
* Tier reassessment: the 233 source is a maintained read-only test checker and tests; 153 is message-only in a retention-deletion control. Because the file is a deletion control, tier is FOCUSED only on the recorded 153 and 233 evidence of unchanged predicates; any logic change would be FULL. Verified by main-relative diff after merge.
* Pending, never retrospectively marked: named human copy and design approvals, assistive-technology and user testing, independent exact-head assessment, hosted CI, owner approval. Original adverse and failed 233 evidence is preserved byte-for-byte.
* Planning Readiness: Ready.
