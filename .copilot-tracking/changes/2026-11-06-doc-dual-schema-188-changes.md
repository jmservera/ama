---
title: Changes for #188 dual-schema documentation correction
ms.date: 2026-11-06
---

* Prospective commit 58de391f (07:29:45Z: Research, Plan, Details and single critique) preceded the first canonical edit.
* `src/core/README.md`: input paragraph names two separately closed branches (13-field `sensor-fault-input-v1` from `READING_FIELDS`; 16-field `live-sim-reading-v1` from `LIVE_FIELDS`, no `calibrated`), scopes the field rules to the indoor branch, states weather/sunlight originals stay in `retained_envelopes`.
* `src/api/README.md`: batch and shared-contract paragraphs name both shapes, link the live simulator container message and `live_readings.py` authority; historical 2026-10-18 measurement labelled historical.
* Research plan: added a dated 2026-11-06 current-use note at the start of "Authority and required observation fields"; historical text, measurements and the 2026-10-18 anchor unchanged; `ms.date` 2026-11-06.
* `docs/reference/README.md`: dated qualification appended to the #186 index entry. `docs/reference/log.md`: one new entry appended; earlier entries untouched.
* Chronology disclosures: my first index edit accidentally dropped the blank line and the start of the following paragraph, and the first API link anchor used a non-existent slug; both were corrected before any check ran. That one anchor correction used a one-line Python text replacement on my own just-written text instead of the edit tool (a process deviation, content only). The api shared-contract wording was reworded once to remove a trailing space and an awkward phrase.
* Checks (light, no heavy gate, SQL, browser, scanner, install; bytecode off), raw outputs under /mnt/ama-gates/i188-doc-dual-schema-r19-1106: `git diff --check` exit 0; source consistency script confirmed 13 indoor and 16 live fields, no `calibrated` in live, version string `live-sim-reading-v1`, ASCII-only added lines, all added links resolve (exit 0); same-file anchors present exactly once; only the five planned documents changed, no `.py` or test diff.
* Limitation of the link check: relative-file links and anchors were checked by a small script, not a full Markdown linter; the script's first-pass same-file anchor check was loose, so same-file anchors were re-checked precisely.
* Not changed or claimed: source, tests, tolerances, consent, calibration, criteria; independent provenance, indoor calibration, statistical, live or owner approval; fresh FULL on the new head (required, coordinator-owned).
