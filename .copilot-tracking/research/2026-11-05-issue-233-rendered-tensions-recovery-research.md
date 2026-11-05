---
title: "Recovery research: issue 233 rendered tension checker"
description: Forward recovery research of the current rendered-tension checker scope and the original late-artifact failure
author: Copilot
ms.date: 2026-11-05
ms.topic: reference
---

This is forward recovery research written on 2026-11-05 at about 18:50Z, before any recovery planning or validation. It is not a retrospective original plan and does not prove that a plan existed before the code. Original, correction and audit records stay unchanged.

## Original process failure (retained, not cured)

* The original checker was created at 13:09:35Z. The original Research was created at 13:12:54Z and the Plan, details, changes and Review at 13:13:16Z, so every original artifact followed the code. Corrections 1 to 3 persisted their artifacts after their code as well. Only correction 4 has Research and Plan written before its code.
* No prospective written plan covering the initial checker was located. The 2026-11-04 #233 artifact sets (choice-before-capacity, withheld-evidence-screens) planned source and copy work and listed rendered checking as not run.
* The read-only audit log is `/tmp/rpi-233-original-phase-provenance-20261105.log` (sha256 `9276117ada98d57fe597934faeafbfd105ea192a091cce379dcce4dcd6c2e4a7`). Original events remain in session 012c42d2.

## Current scope and identities

* Branch `test/atlas-rendered-tensions-233`, HEAD `d540244fe52db2b6ce9bde6b8216639c49eea18f`, tree `74711b6376040d5153feed8b7e0aa27b7379e6f1`. Local parent `test/ux-evidence-149` and fetched `origin/main` are both `bb3a3b03cb94eef6c06ae4b12d07cfe7bbdef43f`. No remote child or parent exists. Local only.
* In scope: `src/api/checks/atlas_tensions_browser_check.py` (530 lines, blob `5e4e2d51b2ad95739a7f89bf070e24eebfa5f846`), `src/api/tests/test_atlas_tensions_checker.py` (102 lines, blob `08151f6f5cab26560d7f83f9c683a0384cb494c8`), the pinned phrase in `src/api/tests/test_role_screens_conformance.py`, and documentation (`src/api/README.md` blob `e2b67cb87f200a92041b0db0f101355ef09d36bd`, `docs/reference/research/ux/atlas-screen-trace.md` blob `9b2f10ec601d8e9ef478fed220b80c972addfe9d`, `docs/reference/log.md`, `docs/reference/README.md`).
* Diff against main (excluding `.copilot-tracking`) is 7 files, 670 insertions and 6 deletions. The six original ignored caches are present and untouched.

## Current behavioural evidence

* The full checker was read end to end on this date. It signs in as a synthetic programme manager through `/app`, opens Programme queue, Resident choice and Package queue for one synthetic home, and checks rendered withheld panels, panel order, fixture-derived choice values, package rows in reference order against a reordered response, read-only behaviour, labelled table regions with Tab reach by region index, and 1280px and 320px layouts.
* Reading found no new functional defect and no assertion that restates a constant. The earlier correction defects (blank labels, label-based reach) are fixed in the current source.
* Historical, genuine but tied to older heads: d540 partial receipt `/tmp/r233i/receipt.json` (sha256 `0b0aedaa82ac59d7e9cd70c5b3208eacbfc50a3da7c47aa76f71eab2cae2a391`), the 194-PASS Chromium run and the duplicate-name DOM probe. They are not re-executed in this loop and become historical for any new head.

## Boundaries

* LIGHT only: another runner owns heavy admission, so no gate, browser, SQL or build runs here.
* C2 engineering only. C4 connected journey, C5 WCAG, AT and user acceptance, and whole #233 and #149 stay unmet. No ticks, closure, push or PR.
* Planning readiness: Ready. Research disposition: executed. Recommendation: retain the existing code unchanged and add recovery records only.
