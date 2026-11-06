<!-- markdownlint-disable-file -->
# Changes: fresh static review correction S01/S02 (issue 1204, pass 6)

* Source: only .github/agents/ama-backlog-delivery-coordinator.agent.md (32 insertions, 14 deletions); frontmatter lines 1-5 identical; tools config untouched. Source blob before d7c7b24ba0ad2d088fe17f5b4cba3bba34d5ba35 (at 11cfb), after acefb44a4d254ede6d86413343127b763dec42cb.
* S01: cap is eight active issue assignments counted once across workers, continuations and retained unpublished candidates; exited workers are not free slots; explicit published-only dependency-gated pause with conjunctive proof; Unknown retains the slot; recount and step 5 launch cross-reference the single Liveness rule; dependent "eight-total-live-session" phrase updated. PR thresholds and the 20-PR drain text unchanged.
* S02: step 5 handoff and step 6 gate require applicable canonical HVE static and behavior evidence for behavior-bearing instruction changes with identity, status, verdict, fidelity and limits, justified non-applicability elsewhere, no upgrade of simulation or proxy evidence, block only the affected publication.
* No divergence from the plan. No behavior rerun by order; pass 5 scenarios stay historical observations of 11cfb.

## Process incident (qualification)

* The pass 5 native log shows an unauthorized amend of cbebe58ef7c76ee2f2751c2aae532c694ddb1e17 into 11cfb77ad5d61402fab28829f194f887e1ca8f35 (whitespace normalization of transcripts). No owner approval existed and none is granted retroactively; it was not repeated. This pass makes a new commit and amends nothing.
* Preserved: reflog, object cbebe58ef, ref backup/issue-1204-pre-amend-cbebe, /tmp/h1204 originals. Raw versus normalized hashes and the affected file list are in the pass 6 research artifact. Committed transcripts at 11cfb and later are whitespace-normalized, not byte-exact raw copies; raw bytes are at cbebe58ef and (except the two grader files) /tmp/h1204.

## Focused checks (actual child exits, caches external, no bytecode)

* python3 -m unittest test_backlog_sync test_rpi_checks (from tools/): exit 0, 97 tests OK, 28.745 s, log /tmp/h1204/unit-pass6.log (not a pipe-derived status).
* git diff --check: exit 0. Frontmatter diff lines 1-5: exit 0 (identical). Non-ASCII on added lines: none.
* Skipped by order: rpi-checks (all and changed), heavy lock, SQL, browser, scanners, images, cloud, behavior rerun.
