---
title: PR 557 IoT test contracts phase details
description: Bounded implementation and validation expectations
ms.date: 2026-10-29
---
<!-- markdownlint-disable-file -->

## Metadata

Task ID: pr557-test-contracts-2026-10-29. Slug: iot-pr557-test-contracts.
Plan: .copilot-tracking/plans/2026-10-29/iot-pr557-test-contracts-plan.md.
Research: .copilot-tracking/research/2026-10-29/iot-pr557-test-contracts-research.md.

## Phase Index

| Phase | Name | Status | Tasks |
| --- | --- | --- | --- |
| P01 | Strengthen live test contracts | Complete, validated | P01-T01, P01-T02 |
| P02 | Validate, independently review and commit | Validation and Review passed; commit remains | P02-T01, P02-T02 |

<!-- rpi:phase id=P01 -->
## P01: Strengthen live test contracts

Only infra/tests/test_iothub_module.py is a source target. Existing
self.live compilation and values/evaluate helpers supply the needed contracts.
No production changes or broad helper extraction. Completion requires exact
compiled objects and observable rejection of incorrect parentage/group.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Assert live compiled parameters and referenced template

Add standard json/subprocess imports and INFRA from test_bicep_policy. Run
az bicep build-params --file str(INFRA / "iot-hub-live.bicepparam") --stdout,
capture text and stderr, assert return code zero. Parse result.stdout, parse
templateJson and compare with self.live. Parse parametersJson and assert its
parameters map exactly equals the four approved {"value": ...} entries.
One positive method is sufficient: compiler failure and equality supply explicit
failure behavior. Template identity is semantic, not a source substring.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Assert full evaluated consumer-group name

The current test_live_profile_never_puts_existing_hub_and_guards_actual_sku
ends with a suffix check. Replace it with a narrow shared assertion called by
that test and one new mutation test. Evaluate group["name"] with
self.values(template), template.get("variables", {}) and compare exactly with
"fixture/events/api-consumer". Mutate a deepcopy, retaining the group suffix
under wrong-hub, and separately use a wrong group under fixture. Each mutation
must raise AssertionError through that same helper.

<!-- rpi:phase id=P02 -->
## P02: Validate, independently review and commit

No Azure calls: az bicep build/build-params are local compiler commands only.
Keep outputs in session scratch when necessary, retain compact original evidence
in the changes record and independent Review.

<!-- rpi:task id=P02-T01 -->
### P02-T01: Run requested selectors and Ruff

From infra, run python3 -m unittest discover -s tests -p 'test_iothub*'.
Run the two existing BicepPolicyTests parameter-contract selectors with the
tests directory on the test import path, after confirming the real class name.
Run python3 -m ruff check infra/tests/test_iothub_module.py from root (or the
equivalent touched-file path from infra). Missing Ruff has already been
observed, permitting dependency restoration without manifest changes.
Completion evidence: all pass with no skips and git diff --check succeeds.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Preserve independent Review and commit locally

Delegate a single independent post-implementation review with exact source diff,
plan, details, critique, changes and command evidence. Reviewer writes only the
new dated review artifact; no implementation or recursive review. Preserve any
findings without a second Review. Classify each finding against the two requested
contracts; any unresolved in-scope acceptance failure leaves delivery blocked or
incomplete, never successful. Route genuinely out-of-scope observations separately.
A local checkpoint commit preserves evidence but does not establish acceptance.
Configure local author and committer email 8036360+jmservera@users.noreply.github.com,
derived from gh api user, then commit source plus original task evidence and
Co-authored-by trailer. Verify commit and clean worktree, no push. Publication
receipt, hosted checks and human approval remain unperformed and unclaimed.

## Unresolved Items

No design blockers. Ruff restored outside repository. IoT discovery passed 22
tests; existing parameter selectors passed 2 tests; no skips. Touched-file Ruff
and git diff --check passed. Independent Review executed once, Complete /
Conformant with no findings, and independently reran the same checks.
Only P02-T02 local commit and verification remain.
