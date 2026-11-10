---
title: Issue 149 axe statement and independent assessment qualification (2026-11-10)
ms.date: 2026-11-10
---

Refs #149 #440. Additive qualification by the coordinator for one process D2 (D1 spent; no D3, no source correction, no budget reset). Not an independent assessment, approval, waiver or new execution. Local only.

## Old statement and correction

* Old literal statement, cutover pack line 6341 at `be5a3b5da`, preserved here: "Axe: ran in the six role-screen stories (the programme stories at 1280 px on `main` only, no violations, `incomplete` empty where reported). It did not run in the atlas, paging or Held download checks, which state so. Automation is engineering evidence only."
* Actual raw evidence (`phase149-coverage-integration-evidence-1110/checks/`, `M1-roles-*.log` and `B4-roles-*.log`): axe lines only for selectors 230, 231, 231q, 231p and 231qp; the default selector ran no axe. The old statement was an overstatement of the evidence count, not a product defect.
* Correction: only that paragraph of the new 149 checkpoint now names the five selectors, excludes default, atlas, paging, Held and human, assistive-technology and WCAG acceptance. Earlier dated checkpoints, the index and the log are unchanged.

## Independent assessments (reviewer `fa061121-54f6-4539-9300-392d0d7f2ed5`)

* Original, `independent-149-integrated-parent-1110/` (ROOT): exact head `be5a3b5daa877f47451350b5117ea758cef7355a`, tree `6bd78a025b19a5b032adb8fe19255b94ff93a3c2`, relative to main `d52f20a5198de7269f39daf794911545aee01ced`; 128 files and 5420 diff lines read in full plus all combined logs; verdict approve_with_comments, 2 Medium, no Critical, High or Low: existing #1362 (atlas checker version assertion can pass for the wrong version; a checker false positive, not a demonstrated product defect) and existing #156 M1 (proposed empty-page versus empty-set ambiguity). Both stay held, unapproved, not repaired and not waived. findings sha256 `f17b788f98905c595fce59654b4eef89f216dc4df9b9e27e284d3e7feae43322`, ledger `074aa619e9707bc01b92f0ede13de343c7c0b0ce8746d91866e54ee49785a303`. Reviewer limits: no fresh guideline retrieval, no independent git or hash execution, no tests, baseline logs not exhaustively read at that time.
* Follow-up, `fresh-guidelines-baseline/`: additive, same head. Root (not the reviewer) retrieved the Web Interface Guidelines in full at 2026-11-10T09:38:16Z, sha256 `d246b026f4f29b5823a9cc857f9edf3d2507002e055e32040cadeaf3b38e0234`; the reviewer did not recompute that hash. All B1 to B5 logs were read; the changed `app.js` hunks pass the fetched guidelines; one NEW Medium documentation-contract finding (the axe statement above), cumulative 3 Medium, 0 Critical, High or Low. findings sha256 `bcdfcf91b15c27f838a7eec96f7274681a51e398903c9b360edf211c91aef70f`, ledger `6b3bf87ca10b1bb1917310541dfa48e2c2061b422f77d7692c7a7fc177c7f55b`, guidelines text `c99f5a07dae3b1a94d73edad239ffba68e21ef05128938e8a97db59dfc9fa52a`.
* Provenance: Root supplied retrieval, hashes and identity; the reviewer's work was static reads of the diff and logs. This D2 is a correction by the coordinator; no future independent D2 pass is claimed, and the same reviewer must still assess the new delta before publication.

## Source identity and carried-forward checks

* `HEAD:src` is `6502cdfe1d181e159a642ea45af9607cf1b294f5`, equal to `0e5758da:src`; unchanged by D1 and D2. No test, install, model, cloud or private-data action was run for D2.
* Original local checks carry forward by that source identity only, run 2026-11-10 about 09:15 to 09:25Z with Python 3.12.3, ruff 0.17.1, mypy 2.4.0, Playwright 1.64.0, Chromium 156.0.8078.4: API unit 194 run, 4 skips, exit 0; handoff browser 9 OK; Core `test_import_refusals test_atlas_screen_trace` 38 run, 7 SQL skips, exit 0; importer 79 OK; static clean; Chromium role-screens, atlas, paging and Held download exit 0 with axe in the five selectors above only. M4a exit 1 (command fault) then M4a2 exit 0 stay preserved. Not a new execution, hosted CI or acceptance.

## Debits and limits

Two process debits (D1, D2); no further grant. #1362 and #156 M1 stay unresolved; no whole 149 or 440, UX, WCAG, AT, human, SQL, model or cost claim.
