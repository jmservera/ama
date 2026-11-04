<!-- markdownlint-disable-file -->
# Research: issue 946 inaccurate error message (workflows.py:437)

Disposition: executed. Planning Readiness: Ready.

## Prior delivery check

* Merged PRs found by searching issue 946: only #777 and #919, which mention the number incidentally and do not touch the hazard receiver. No merged PR delivered this issue. Nothing to redo.

## Evidence

* The issue cites `workflows.py:437` from the review of #898. At #898 (commit 871f2f45a) line 437 is `accept_hazard` and the nearest inaccurate message is in `_hazard_receiver` (line 423 then, line 419-426 now).
* Condition: `(h["released"] and not allow_released) or not h.get("referral_version")`. Message: "Record a prospective evidenced referral before continuing."
* The message is wrong when the safety issue has a referral and its retrofit hold has already been released: the user is told to record a referral that exists. `accept_hazard` (line 442, "Record receipt first; acceptance can only be recorded once.") names both of its conditions and is accurate.
* Assumption: the reviewer's line number drifted and the receiver message is the intended target. Flagged in the PR for the owner.

## Scope

* Smallest fix: split the combined condition into two checks, each with a message naming its own condition. Applies to receive, accept, observe times, record repair (all callers of `_hazard_receiver`). No behaviour change beyond the text; both branches still raise `ValueError`.
* Not security, infrastructure, SQL or deployment: focused tier.

## Acceptance criteria

* Message accurately names the failing condition: met by code and test.
* A test asserts the message text: met.
