---
title: Research for #188 parent 184 refresh and operational wrapper r12
ms.date: 2026-11-06
---

* Research disposition: executed (read-only git inspection after a fresh fetch of main and parent 184; no SQL, Docker, test, gate or install). Planning Readiness: Ready. These records are committed before any merge, test or wrapper action.
* Intake: child head e97ab551cb7a4108231a9413ade1168efcf737a6, tree 46b6e2a3df75812871337721646be7844df0dd2b, ignored-inclusive status empty. Fetched origin/main bb3a3b03cb94eef6c06ae4b12d07cfe7bbdef43f. Fetched parent 184 2dc125f9721e785d8b99a150f4297ff91bff63ac, tree b91080054c9726f887b7e7dd4f8b76c576e4fd87 (PR 1205 squash, parent-only engineering integration, not main, live or credential-owner acceptance). The child merge-base with the parent is bb3a3b03c.
* Parent change surface (21 files, 407 insertions): `src/core/src/zava_forward/core/synthetic/device_provision.py` (new), `src/core/tests/test_device_provision.py` (new), `src/core/README.md` (+11), and #185 RPI records. The child's change set overlaps the parent in one file only: `src/core/README.md`, where both sides add text. Sensor, consumer, ingestion, verifier and SQL helper sources are untouched by the parent, so child sensor coverage stays unchanged.
* r11 chronology gap (preserved, not repaired): the r11 wrapper was copied, edited and compiled before its HANDOFF.md Research and Plan were written, so that written planning was not prospective. r11 and its author claim stay unchanged. Earlier history also stands: the original ingest was post-hoc, the weather loop and the r9/r10 sensor SQL coverage correction were genuinely prospective.
* Source coverage: existing SQLite constructed sensor tests (consistency, live consumer, ingestion; 102 tests earlier, zero skips) plus the parent's device tests. Actual SQL remains unexecuted for every selector; the wrapper's first run is untested.
* Tier: FULL (ingestion, SQL, runtime). Heavy deferral: #82 owns the heavy lock with a running gate. This continuation is light only: no SQL, Docker, gate, `--changed`, install, scanner or browser, and no lock use.
* Wrapper delta needed (r12): repin HEAD and TREE to the final frozen head; add a guard comparing the declared remote parent 184 head to the pinned 2dc125f9, separately from origin/main bb3a3b03c, at every fetch check. `--base` for FULL stays current main; the parent is never the reviewed base.
* Out of scope: sensor, runtime, consent, calibration, SQL schema or credential changes; refactoring; new frameworks.
