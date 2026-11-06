---
title: Plan for #188 dual-schema documentation correction
ms.date: 2026-11-06
---

* Step 1: `src/core/README.md` input paragraph: state two separately validated closed branches selected by `schema_version`: `sensor-fault-input-v1` (13 fields, `READING_FIELDS`, indoor, with `calibrated`) and `live-sim-reading-v1` (16 fields, `LIVE_FIELDS`, synthetic outdoor weather, no `calibrated`), each rejecting the other's key set. Keep the indoor field and ID rules, scoped to the first branch. Link the live schema authority (`live_readings.py`, `sensor_consumer.py`).
* Step 2: `src/api/README.md` batch paragraph and shared-contract paragraph: observation fields come from `sensor_faults.Packet.rows` (13) or the live-sim reading envelope (16); link the live schema authority and the existing live message description. Retain stock-ID and no-wire-adoption caveats.
* Step 3: research plan "Authority and required observation fields": add a dated 2026-11-06 supersession/current-use note before the historical text, pointing to the 2026-11-05 weather section and the two authorities; keep the 2026-10-18 measurements and heading unchanged. Qualify the sentence "only `sensor-fault-input-v1` is accepted" as the historical single-schema state with an explicit pointer.
* Step 4: `docs/reference/README.md` index: extend the existing #186 pointer with a dated qualification link; append one `docs/reference/log.md` entry (no earlier entry rewritten, no new page).
* Step 5: planned light checks only: `git diff --check`, relative-link and anchor resolution for touched files, source-consistency script asserting 13 and 16 field counts and the quoted authority names against source, ASCII-punctuation check on added lines, confirm only the planned files changed and no source/test diff. No heavy gate, SQL, browser, scanner, install.
* Step 6: Changes record, then a separate later author Review and state; commit with gh-api-user-derived repo-local identity and Copilot trailer; verify ignored-inclusive clean.

## Critique (single, final candidate, before implementation)

* Compatible, applied: keep the statement about exact counts anchored to source names rather than invented prose; scope indoor ID/length rules to the indoor branch only; do not claim the live branch is calibrated or indoor evidence.
* Compatible, applied: the supersession pointer must not delete or reword historical measured values.
* No conflict with confirmed decisions; no significant or divergent issue requiring a user decision.
