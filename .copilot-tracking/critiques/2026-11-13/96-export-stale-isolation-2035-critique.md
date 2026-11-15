---
title: Issue 96 criteria 5 and 6 plan critique
description: Single independent plan critique and dispositions; not repeated
ms.date: 2026-11-13
---

One independent read-only rubber-duck pass on the frozen research, plan and details. Verdict: revise. No user decision required: every finding is compatible with the owner direction (no invented dependencies, no authority).

| Id | Severity | Finding (as returned) | Disposition |
| --- | --- | --- | --- |
| PC-001 | Blocking | Calculated fields are conservatively treated as dependent on any changed field because calculation inputs are undeclared, so strict selectivity is not proven | Accepted as scope. Criterion 6 is proven only for declared dependencies (field definitions, `required_when`, bound sources, per-field calculation reference); the conservative cause is labelled `calculation-inputs-undeclared` and tests assert that label. No dependency is invented; the issue criterion is not claimed closed |
| PC-002 | Blocking | Approval transition not shown; `area` already carries an open calculation issue before the change | Accepted. Tests assert baseline then after for epc and notes approvals (Current to Review required with causes); area approvals are excluded from isolation claims and its baseline is asserted separately |
| PC-003 | Significant | Unknown or unscoped entries can show as None recorded in the UI | Accepted. The panel counts unscoped and Unknown or Unavailable proposals and approvals explicitly |
| PC-004 | Significant | View cost and failure surface grow | Accepted. Proposals share the report digest cache and sit inside the existing DocumentUnavailable guard; a multi-draft and unavailable-evidence test is added |
| PC-005 | Significant | Area proposal Current while its approval needs review is ambiguous | Accepted. Documented and tested as intended: a proposal is bound to its source and definition; an approval also follows the dependent open validation issue |
| PC-006 | Note | View addition does not change the export digest | Accepted. Added a digest stability regression assertion |
