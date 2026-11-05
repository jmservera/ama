---
title: Sensor checkpoint recovery details (Refs #440 #184 #110)
description: Phase details and required content of the stabilization record
ms.date: 2026-11-05
ms.topic: reference
---

## Phase 1 required content of the evidence-pack section

* Trigger and identities: window trigger (a due #184/#110 sensor checkpoint after merged #1209 and #1210 and the live simulator slice), main `c6d5a8f3`, tree `876679c3`, working base `3d7ad2fe`, delta tooling-only, document and ADR table (status, version, date, blob), document-qualified IDs.
* Covered and excluded: #1209 and #1210 covered as tooling only; #1203, #1205 and #128 excluded as unmerged; candidate limitations labelled separately and never promoted.
* Traceability table: approved planned feature (PRD FR-050/AC-066 to AC-068, BRD FR-048/AC-090/RULE-014, ADR 0003 decision 6) to main code and tests (source-inspected paths and blobs), observed journey class, remaining backlog owner.
* Contract section: raw weather and wire versus indoor observed series; units; timestamps; identifiers; schema joins; representation and handover compatibility; absent calibration evidence.
* Retention and handover section: retained-beginning replay, SQL as durable state, expiry limit, uncoordinated receivers, commit uncertainty, poisoned envelope, unsupported windows not a pass.
* Evidence classification table per finding (local observed, Azure observed, implemented-unverified, deferred, blocked, unknown) with date and source.
* Actual commands, exit codes and not-run list (recorded after validation, from real output).
* Disposition: continue, fix (named owners and lanes), proposed pivot awaiting owner approval; exact #184, #110, #188, #440 closure and expansion gates; resume conditions; no new defect.

## Phase 2

* `docs/reference/README.md`: one sentence near the existing #110/#184 entries linking the new section anchor.
* `docs/reference/log.md`: one new dated entry at the end; earlier entries untouched.

## Validation

* `git show c6d5a8f3:<path>` blob IDs equal those cited.
* Markdown link and anchor check over the three changed docs (local script, read-only).
* `git diff --check`, `git diff --stat`, `git status --short --ignored` clean after commit.
* Not run: `tools/rpi-checks.py`, unit suites, SQL, Docker, Chromium, FULL, cloud calls.
