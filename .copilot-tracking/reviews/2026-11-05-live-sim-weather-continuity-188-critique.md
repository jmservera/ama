---
title: Plan critique for #188 synthetic weather continuity
ms.date: 2026-11-05
---

* Critique executed once, inline, on the final candidate plan before implementation. Verdict: proceed with applied findings.
* Finding 1 (applied): tolerance bounds must not be fitted. Derive only from declared generator constants and state wide-envelope limits and the unapproved status in the output.
* Finding 2 (applied): do not duplicate the comparison; extract and share it so legacy `report` output stays identical, proven by the existing handover tests.
* Finding 3 (applied): reject, never drop: mixed windows, mixed or cross-schema references and wrong scenario/unit are refusals before statistics or replay writes.
* Finding 4 (applied): reference provenance cannot be verified from rows (same anchors assumption); report it as a declared assumption, not proof.
* Finding 5 (applied): refuse explicit non-zero tolerance flags on the weather path instead of silently ignoring them; no new flag.
* No conflict with the owner decision. Not claimed: physical calibration, live Azure continuity, C1/C2 or 188/184 acceptance.
