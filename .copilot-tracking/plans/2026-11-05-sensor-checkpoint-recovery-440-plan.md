---
title: Sensor checkpoint recovery plan (Refs #440 #184 #110)
description: Plan for one dated current-main sensor contract, retention and handover stabilization record
ms.date: 2026-11-05
ms.topic: reference
---

* Scope: append one dated section to `docs/architecture/cutover-evidence-pack.md`; add one dated index sentence to `docs/reference/README.md` and one append-only entry to `docs/reference/log.md`. No code, coordinator, workflow, case study, issue or remote change. Local commit only.
* Phase 1: append "Fifth stabilization checkpoint: current-main sensor contract, retention and handover (2026-11-05, Refs #440 #184 #110)" at the end of the evidence pack, preserving all earlier sections.
* Phase 2: add the index link and the log entry (append-only).
* Phase 3: focused validation only: relative link and anchor check on changed Markdown, `git diff --check`, `git diff --stat` confined to documentation and tracking paths, blob identity re-resolution against `c6d5a8f3`, em dash and non-ASCII scan of added text. No heavy SQL, image, browser, FULL or `rpi-checks.py` run (heavy lock owned by native FULL gate; a fail-fast attempt is also not made).
* Phase 4: one independent review of the committed-candidate diff by a read-only agent; record outcome; commit tracking artifacts with noreply identity and Copilot trailer; verify clean `git status --short --ignored`.
* Evidence classes used: local observed, Azure observed, implemented-unverified, deferred, blocked, unknown. Source inspection is never executed acceptance.
* Critique: executed once, see [critique](./2026-11-05-sensor-checkpoint-recovery-440-critique.md). Details: [details](../details/2026-11-05-sensor-checkpoint-recovery-440-details.md). Research: [research](../research/2026-11-05-sensor-checkpoint-recovery-440-research.md).
* Closure rule: use `Refs #440`, `Refs #184`, `Refs #110`; never a closing keyword. #440 C7 and C8 stay unticked.
