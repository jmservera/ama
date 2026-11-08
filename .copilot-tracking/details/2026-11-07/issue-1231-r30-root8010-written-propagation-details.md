# Issue 1231 r30 propagation: details

Plan: .copilot-tracking/plans/2026-11-07/issue-1231-r30-root8010-written-propagation-plan.md

## Step 3 merge

Expected conflicts: ranking README, helper, runner (add/add), Store, core tests, API wiring test. Resolve with the child's blob, then apply step 5 by hand. Verify no conflict markers and that non-ranking content equals root 8010.

## Step 4 red tests (adapted, child-owned stage prefix; none skipped or proxied)

* test_ranking_publication: written is True on the first-write error and None for a bare error; retry of an existing record raises with written False and original published_on; race loser raises with written False and the winner's date.
* test_ranking_publication_runner: first-write sync failure gives committed_unconfirmed, exit 2, written True; unconfirmed retry gives written False and the same path; message path-free; record kept and verify clean.

## Step 5 source

* DurabilityUnconfirmedError.__init__(path, published_on, cause, written=None); self.written.
* _confirmed passes outcome["written"] and copies stage_retained to the error.
* Runner: except DurabilityUnconfirmedError before the PublicationError/OSError handler; out status committed_unconfirmed, uncertainty code/message/next_action (+ stage_retained when present). main returns EXIT_REFUSED for that status.
* README: adopt the root paragraph, keeping the child's stage_retained sentence.

## Evidence

External logs in /mnt/ama-gates/g1231-r30-prep-1107/logs, one exit file per command.
