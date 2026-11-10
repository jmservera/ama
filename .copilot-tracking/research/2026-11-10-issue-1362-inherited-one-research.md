---
title: "Research: issue 1362 inherited one correction (exact Current design version field)"
description: Authority proof, current-main baseline and false-positive evidence for the single inherited #233 to #1362 checker correction
author: Copilot
ms.date: 2026-11-10
ms.topic: reference
---

Task: `issue-1362-inherited-one`. Branch `fix/demo-atlas-version-1362-1110`, worktree `issue-1362-current-version-1110`, created from main `0a6dc0b3f0b3ecf098536369a8308b02226b98b8`. Research disposition: executed (targeted; the D1 diagnosis is reused, not repeated).

## Authority (Root, 2026-11-10)

* Source: Root `1362-one-inherited-correction-1338.txt` and `demo-1362-minimum-authority-assessment-1334.txt`, read in full, plus the 2026-11-10 reconstruction (`provenance-1362-authority-ledger-1322.md`, `handoff-1362-authority-reconstruction-1322.md`), which stays UNKNOWN as history.
* Owner directions, 2026-11-09: 08:00:39Z repository default of five total cycles per issue (event b54f17c3); 08:02:51Z "add 5 additional cycles to exhausted issues" (event 4ce1caa5).
* Inherited history: four named Nov 5 corrections (KB index, lint, non-blank labels `18f38e8de`, region identity `d540244fe`) plus one possible Nov 5 chronology-recovery debit. Let d be the charged count. If d <= 4 the default leaves at least one; if d = 5 the issue was exhausted before Nov 9 08:02 and the extension of five applies. Nov 10 two-screen (initial), record recovery (metadata) and the D1 diagnostic (read-only) are not debits. The manager confirmed no later contrary debit or owner exception; a named allocation is not required.
* Proven minimum: at least ONE unused inherited cycle. Exact balance remains UNKNOWN. This task consumes that one; the conservative proven remaining minimum afterwards is zero, with no automatic second correction or self-retry. It is not a fresh C1, not a fresh five and not a reset, and it does not borrow the #135/#1360 zero.

## Scope and constraints

* Only `src/api/checks/atlas_tensions_browser_check.py` (the exact Current design version dt/dd assertion) and direct regressions in the existing `src/api/tests/test_atlas_tensions_checker.py`.
* No app, panel, CSS, fixture, version-schema, role, identity, policy or backend change. No #1360 post-commit fix. Focused owner demo tier, not the full or `--changed` gate. No assistive technology, WCAG, usability or production acceptance.

## Current-main baseline (identity)

* HEAD `0a6dc0b3f0b3ecf098536369a8308b02226b98b8`. Checker blob `e3aa479048bd0f7884151e0533d9ddbf11703dcf` and unit test blob `9774b84acedc9fa9fd9f14bc130ccf4e57248a44`: identical to the D1 diagnosed blobs at `aaec7b0bd` and to the frozen #233 witness. `git diff aaec7b0bd 0a6dc0b3f` over both files is empty. The checker is therefore not already fixed and not materially different.
* Defect site: `check_technical` loops over `str(technical["design_version"])`, `design_name` and the last note and asserts each is a substring of the whole Design version panel text. The renderer (`role-screens.js`, `screenFields`) emits exact `dt`/`dd` pairs: `Current design version`, `Recorded by`, `Recorded at`, `Latest change note`. The product renders correctly; the defect is a constructed checker false positive, not a product defect.

## Already-proven D1 evidence (reused; `ROOT/handoff-1362-version-diagnostic-1110.md`)

* With the unchanged checker, mutating only the associated dd: `10` and a duplicate label wrongly pass on the natural fixture; `2`, `Unknown`, empty and missing label wrongly pass when recorded-at (or note) supplies a `1`. Positive control passes. The first D1 run had a harness leak (no reload) and is preserved as adverse; the Playwright 1.64.1 install against the declared 1.64.0 pin remains adverse for D1.

## Planning readiness

Ready. The current-main baseline will be re-executed as step one of Implement before the edit (checker identity, positive control, and the false-positive classes), using the declared pins in an owned environment. If that baseline shows the false positives are absent or materially different, STOP.
