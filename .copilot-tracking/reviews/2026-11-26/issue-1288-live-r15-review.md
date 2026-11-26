---
title: Issue 1288 live r15 review
description: One post-implementation review
ms.date: 2026-11-26
---

Review executed once. Outcome: conformant for the stated scope; no claim of live acceptance.

* Fix is narrow: only the demo override (profile plus exact value) lifts the assistants hold; `gate_hold` fail-closed and the open record remain. Test proves base failure and non-demo hold.
* Azure write reverted and verified (no ZF_ASSIST allowance variables, revision Healthy). No secret in artifacts.
* Routed follow-up: deploy a build with the fix (needs registry access or owner network decision), set the same finite allowance, run one walkthrough for criteria 4 and 8. Criteria 4 and 8 stay unticked.
