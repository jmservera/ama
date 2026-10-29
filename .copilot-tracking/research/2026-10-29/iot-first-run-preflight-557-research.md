---
title: IoT first-run preflight research for PR 557
description: Focused evidence for Copilot comment 4418722664
ms.date: 2026-10-29
---

<!-- markdownlint-disable-file -->

## Research Brief

* Topic: PR #557 first-run quota, cost headroom and active-alert preflight.
* Purpose and audience: make the bounded exercise instructions safe for the operator of a reused hub.
* Scope: `src/api/README.md` and directly relevant local contracts. Documentation only unless existing code cannot express the requirement.
* Non-goals: Azure access, runs, deployment, credentials, issue acceptance, push or edits to rubric scores.
* Criteria: verified current quota usage explicitly supplied as `daily_used_units`; >=40,000 units retained; remaining cost headroom and actual active alert verified before the one approved run; existing limits preserved.
* Output mode: convergence, preparing planning.

## Research Parameters

* Posture: focused, selected from the named finding and two supplied documentation targets.
* Resolved evidence root: `.copilot-tracking/research/2026-10-29/`.
* Prior knowledge: user finding verified against PR comment 4418722664 and the named source documents; memory is context, not evidence.
* Candidate internal areas: API first-run guidance, core replay budget, publisher and existing local tests, research cost section and infrastructure approval.
* Candidate external areas: exact GitHub review comment only; no external technology or regulatory research needed.

## Extension Registry and Provenance

* Selected: repository instructions (branch, privacy-safe identity, dated evidence, local gate), `rpi-research` and its reference/template, RPI state contract.
* Selected later: `rpi-plan`, `rpi-implement`, `rpi-review`; independent critique and Review only where required by those protocols.
* Skipped: domain/cloud/security/UI skills and research delegation; this is a small, coupled local documentation trace, not deployment, legal research, vulnerability assessment or web work.
* No matching `copilot-tracking.instructions.md` exists in the checkout.

## User Participation and Research Decisions

* No intake question: the explicit full-loop request, scope and no-push/no-Azure limits are sufficient in this non-interactive session.
* Active controls: docs-first; preserve single call, two messages, 1/s, 60s and October 31 cutoff; no live quota/cost/alert observation is authorized.

## Research Cycle Log

### Cycle 1

* Wider: read original/addendum, reference index and memory; verify exact GitHub comment and existing quota/cost research. Reflection: the missing operator preflight is distinct from the already documented single-run and cutoff restrictions.
* Deeper: read C3/C4 and publisher validation. `daily_used_units` defaults to zero, is a nonnegative integer, and participates in the existing per-run B1 quota guard before sends. Reflection: verified usage can be supplied without changing code; a reference string cannot establish current quota.
* Contrarian: considered changing the default or runtime to retrieve quota automatically, and merely linking the research section. C3/C4 show existing nonzero-usage rejection; C5 preserves separate live authorization. Reflection: neither runtime change nor a link-only fix is justified. Explicit fresh preflight, conservative accounting and stop conditions close the operator gap without new cloud authority.
* Parent synthesis: accept C1-C5/W1; document actual-use input, remaining cost headroom and active alert verification before constructing the single-run budget. Reject invented usage, assumed-zero reuse, automatic cloud lookups or expanded run authority.
* Re-entry: no further cycle needed. All focused questions have local evidence; actual live observations remain intentionally unperformed, not planning blockers.

## Evidence Log

* C1: `src/api/README.md:943-972` records the hub-only activation, explicit finite budget and one-run/cutoff instructions but omits current quota and actual cost/alert verification.
* C2: `docs/reference/research/iot-sensor-analytics-research-plan.md:102-125` requires named-owner verification of currency, aggregate headroom, consumed quota and active alerts; a reference is not proof of an alert.
* W1: https://github.com/jmservera/ama/pull/557#discussion_r4418722664, retrieved 2026-10-29 with `gh api`; exact finding matches user scope.
* C3: `src/core/src/zava_forward/core/synthetic/sensor_stream.py:94-134` defines default usage zero and checks `units + daily_used_units + reserved_headroom_units <= 400000`; each body plus 1024-byte reserve is rounded to 4096-byte units.
* C4: `src/core/tests/test_sensor_stream.py:222-239` rejects consumed quota of 360000 for nonempty frames; `src/api/src/zava_forward/api/iot_stream.py:375` validates before the publisher sends.
* C5: `infra/README.md:3217-3278` limits existing B1/one-unit reuse to USD5 additional through October31, with USD1 hub/USD1 shared metrics-job/USD3 contingency estimates; registry and reachable-path approval remain unresolved.

## Findings Mapped to Questions and Evidence

* Q1: What is missing? C1/C2/W1 support an explicit fail-closed operator preflight rather than merely required reference strings.
* Q2: Can the existing budget express verified daily usage? Yes, C3/C4; pass the verified current daily count explicitly.
* Q3: Is code necessary? No, C3-C5; this request is an operator-documentation correction, not a new verification client or change to shared defaults.

## Alternatives and Decision State

Selected: a focused preflight paragraph next to the explicit single-run budget, with verified usage included in the documented constructor and a link to C2. Require named-owner evidence, measured quota/current reset window, conservative other-traffic/uncertain-attempt accounting, remaining cost/currency/active alert verification and fail-closed missing evidence.

Rejected: code change (C3/C4 already implement the intended guard); link alone (C1/W1 require an explicit operator action); assuming a new/idle hub (C5 records reuse).

## Open Questions, Risks, and Residual Uncertainty

* Actual quota, cost and alert status are unknown and out of scope; documentation must not imply they were verified.
* Complete publication gate and human/hosted approvals remain distinct from this documentation correction.

## Planning Readiness

* Research disposition: executed, complete.
* Planning Readiness: Ready, supported by C1-C5/W1.
* Self-check: questions answered; three ordered inline waves and alternative dispositions recorded; no delegated lane, source edit, Azure call or fabricated measurement.
* Parent handoff: Plan a docs-only change and independent critique. Validation should cover the exact input name, quota inequality, cost/alert evidence, stop behavior and preservation of existing bounds.
