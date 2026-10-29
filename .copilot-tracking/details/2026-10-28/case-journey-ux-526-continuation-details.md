---
title: Case journey 526 continuation phase details
description: Current evidence reconciliation before independent review
ms.date: 2026-10-28
---

Task 526, stable slug case-journey-ux-526. Current continuation plan and changes
are canonical; original phase details remain the behavioral/assertion contract,
not the current status record. The user increases lock admission to 60 minutes
with unchanged 60-second nonblocking retries and immediate release.

## P03 completion

The exact API discovery passed 1156 tests with 314 opt-in skips. Current
journey-05 passed all 37 pinned axe scans, native manual-tab keyboard,
keyboard draft accept/edit/reject and blocked final-check refusal, actual
chrome.tabs.setZoom=2, all nine tabs at 200% with fully visible focused controls,
and 320/390/1280 reflow. Summary bottom is 674.78125 at desktop and
1581.96875 at 320x800 (required <=800 and <=1600). No font shrinking, text
truncation, hidden record or relaxed threshold was used.

Design-system (which also runs workbench), employee recovery, provenance,
regulatory 19-state pinned axe, all five challenge variants and assistant
22-scenario checks passed across the documented admitted runs.
Latest targeted semantics: 23 passed. API Ruff/format/mypy (92 files), runner
30-test regression/Ruff/100-column format/strict mypy, scoped src-ci actionlint
and git diff --check pass. Unscoped actionlint exposed existing generated-workflow
and private-label diagnostics; the gate uses its existing explicit config/list.

## Corrections and review boundary

Compact mobile summary padding/gap/line spacing preserves 16px text and complete
values. Focused tabs explicitly scroll fully into their named overflow region,
including their focus margin at real 200% browser zoom. Harnesses follow tabs
and current role policy; assistant tests install the existing synthetic-only
release fixture rather than weakening runtime release admission. Local gate
parity now includes the hosted journey harness and validates its bound report.
All adverse logs and earlier tracking artifacts remain unchanged.

## P04 execution

Independent Review compares the entire original feature plus continuation
corrections against issue/design, original critique dispositions and current
validation. No source mutation during Review. Route findings to a later
implementation invocation; preserve original verdict. Final full-tier gate,
receipt verification at current main, exact-head assessment, push and PR are
still pending. Screen-reader, real staff usability and deployment remain owner
acceptance, not local failures or inferred approvals.
