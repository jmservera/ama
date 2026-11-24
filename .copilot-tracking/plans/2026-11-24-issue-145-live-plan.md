---
title: Issue 145 live plan (2026-11-24)
description: Plan and single critique for the release-change register that makes restore reapply suspended and revoked releases.
ms.date: 2026-11-24
---

Refs #145. Task `issue-145-live-20261124T041605Z`. Research: [research](../research/2026-11-24-issue-145-live-research.md). Details: [details](../details/2026-11-24-issue-145-live-details.md).

## Phases

* [x] P1 Research (disposition executed, Ready).
* [ ] P2 Add `record_release_change` and `reapply_release_changes` to `recovery.py`.
* [ ] P3 Call `record_release_change` before SQL change in `assistants.change_release` and the attestation suspension.
* [ ] P4 Tests in `src/core/tests/test_recovery.py`; run core recovery, release and assistants tests, mypy, ruff.
* [ ] P5 Update `src/core/README.md`, the runbook step and the knowledge-base log and index.

## Critique (executed once, final candidate)

Verdict: accept with direct dispositions.

* Register entry must not be written for an invalid request: record only after `authorize`, for status in (suspended, revoked) and a release row that exists. Applied.
* A failed SQL change after a recorded entry leaves a stale entry. Applied: reapply only moves `active` to suspended or revoked and `suspended` to revoked, so a stale entry for an unchanged release would wrongly suspend it. Mitigation: record inside the same flow after the SQL change succeeds is unsafe (crash loses it); instead keep entry-first and on SQL failure leave a clearly harmless-by-design entry? Rejected as unsafe. Disposition: write entry first, and if `rel.change` raises, the raise rolls back the transaction and the entry is written as `status` with an `outcome` field not used; to avoid wrongful suspension the pre-check (row exists, status allows the change) is made inside the same transaction before recording, so `rel.change` can only fail on a database error. Accepted residual: a database error after the entry leaves a stricter-than-applied state, which fails closed (the release stays denied, a human can record a new release).
* Entries hold no free text, so the register carries no personal data. Applied.
* Spent allowance and legal hold remain unproven; no design exists. Recorded.
* Wiring `reapply_release_changes` into an automatic restore path is out of scope; no restore automation exists in `src/` (reapply_deletions is also run by the runbook). Runbook step added.

## Validation tier

FULL by classification (release authority path). Local targeted tests and static checks only; the coordinator owns `rpi-checks.py --all`. Hosted CI and independent review remain required.
