---
title: IoT first-run preflight phase details
description: Bounded documentation implementation and verification details
ms.date: 2026-10-29
---

<!-- markdownlint-disable-file -->

## Metadata

* Task ID: pr-557-comment-4418722664
* Task slug: iot-first-run-preflight-557
* Related plan: .copilot-tracking/plans/2026-10-29/iot-first-run-preflight-557-plan.md
* Evidence: .copilot-tracking/research/2026-10-29/iot-first-run-preflight-557-research.md C1-C5/W1

## Phase Index

| Phase ID | Name | Status | Detail sections |
| --- | --- | --- | --- |
| P01 | First-run preflight documentation | Complete; ready for original Review | P01-T01, P01-T02 |

<!-- rpi:phase id=P01 -->
## P01: First-run preflight documentation

Context: the reused B1 hub's daily usage is unknown to the local budget; nonempty cost and alert references do not establish active live controls.

Intent: enforce an explicit operator prerequisite in prose, not introduce a cloud lookup, new authority or runtime default change.

Boundaries: API README and dated RPI records only. No test removal/addition, generated output, Azure access, credentials, private data, rubric hand edit, push or approval claim.

Dependencies: final-candidate critique, followed by existing local budget behavior and preserved exercise authorization.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Require actual preflight evidence and explicit quota input

* Target: bounded exercise paragraph in `src/api/README.md`.
* Explain that named owner must freshly verify current usage on the exact reused hub for the UTC quota day, count other traffic and uncertain attempts conservatively, and require >=40000 units left after run accounting.
* Explicit constructor input: `daily_used_units=verified_daily_used_units` with existing `max_messages=2, max_per_second=1.0, max_seconds=60.0`.
* Verify actual remaining aggregate cost headroom and currency against the bounded allowance/window, plus enabled alert's correct scope, threshold and recipient. Link existing research cost section.
* Unknown/stale/insufficient evidence stops; never imply references or local budget actively measure cost/quota/alert state.
* Preserve one run, no repeats/concurrency/retry, cutoff and separate device/network/role approval boundaries.
* Completion: focused README diff meets AC1-AC4; explicit usage and preflight checks added, surrounding text unchanged. Unresolved items: none.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Validate prose and record implementation evidence

* Validation owner: implementing parent.
* Read changed paragraph against C2/C3/C5 and verify the link and existing constraints.
* Run `git diff --check`; inspect exact changed paths and rubric equality to main.
* Record actual commands/outcomes in changes; mark plan/details tasks only when supported.
* Independently review once after implementation, before commit; later findings are routed, not a second Review.
* Commit original dated evidence plus implementation with authenticated user's noreply identity and Copilot trailer. No push.
* After committing, fetch main and attempt complete gate with a new external output path and nonqueued shared-lock admission. Retain external output; verify a receipt only if generated. A gate failure must be stated, never turned into success.
* Completion: semantic comparison, exact-input/bounds assertions, reference file/anchor check, JSON parse, unchanged surrounding text and rubric equality all passed; `git diff --check` exit 0. No executable files changed or runtime test cases added. Changes record reconciled for original Review.
* Lifecycle closeout remains Review, local commit and complete local gate attempt; live/human/hosted approval is not established. Actual gate availability remains unknown until attempted.
