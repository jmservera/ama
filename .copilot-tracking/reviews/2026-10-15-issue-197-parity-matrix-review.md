---
title: Issue 197 parity matrix review
ms.date: 2026-10-15
---

* Review executed once. Outcome: conformant with open owner decisions.
* Checked: all 125 tracked files present; counts in the matrix (46 test rows, 42 module rows, 15 prototype tests, 72 sandbox files in PR 287) agree with the repository and the PR file lists.
* Findings routed to later work: ADR 0006 alignment of targets; service-role denial test once agents, orchestrator and importer exist; reopen #151 and #175 (owner action); hold PR 287.
* Limits: PR 287 assessed from metadata only; acceptance-criteria judgements rest on PR bodies and repository evidence.

## Review of the fix iteration

* Review executed once. Outcome: conformant with open owner decisions (amendments A1 to A5).
* Checked: coverage script found all 128 real tracked files in the matrix and 450 sandbox files covered by the retire pattern; no `devtools` target remains; counts (719 tests, 92 skipped) from a run on 2026-10-15.
* Findings routed to later work: owner decision on A1 to A5; `fix/remove-assistant-test-sandboxes` pull request (S1); reopen #151 and #175; service-role denial test.
* Superseded: the earlier finding "hold PR 287" (PR merged 2026-10-15).
