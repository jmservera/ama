---
title: Issue 108 corrective phase details
description: Prospective phase details for the serving-evidence clarification
ms.date: 2026-11-07
---

## Phase 3 edits

* In "Semantics that limit what the metadata can prove", replace the `NoAutoUpgrade` bullet's last sentence so it says: the configured version is stable but not an attestation of the version that served a call; the provider response `model` recorded on a real call can inform version confirmation.
* Add one bullet: a response model identifier does not by itself attest the physical processing region or data residency; that needs source-qualified provider or operational attestation and the relevant named approvals.
* In "Remaining #108 gates", split "serving attestation" so version confirmation and region/data-residency evidence are separate and a call does not close the region gap.
* Append one log entry after the last entry; do not edit earlier entries.

## Phase 4 checks

* `git diff --check`, ASCII, relative links and anchors of changed files, diff limited to the planned files. No gate, SQL, browser, image or scanner.
* One Review of the final diff; new state records the order acknowledgement and the follow-up correction.
* Critique: [critique](../../reviews/plans/2026-11-07/issue-108-serving-evidence-correction-plan-critique.md).
