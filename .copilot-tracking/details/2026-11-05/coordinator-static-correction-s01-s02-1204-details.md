<!-- markdownlint-disable-file -->
# Details: fresh static review correction S01/S02 (issue 1204, pass 6)

Written 2026-11-05T23:18Z before implementation.

## Phase 1 (S01)

* Replace the admission unit "live issue sessions plus candidates" with an active issue assignment, counted once across workers, continuations and retained unpublished candidates; an exited worker is not a free slot.
* Add the published-only dependency-gated pause as an explicit disposition releasing the slot only when all hold: local head equals published head or a reviewed squash tree or GitHub merge proof exists; no live native worker; no outstanding unpublished implementation; artifacts, ledger and disposition preserved. The published PR and parent stay monitored. Missing upstream or failed Git evidence is Unknown and retains the assignment.
* Recount sentence counts assignments (open PRs and tmux are evidence inputs, not the unit). Step 5 launch sentence cross-references the Liveness rule. PR thresholds unchanged.

## Phase 2 (S02)

* Handoff: append that a behavior-bearing instruction change also returns applicable HVE static and behavior evidence with exact source identity, execution status, verdict, fidelity and executor or profile limits, or a justified non-applicability.
* Step 6: before publication require that evidence; simulation, emulation or proxy never counts as native-host or stronger-profile acceptance; missing required evidence blocks only the affected publication; original adverse evidence, exact-head and published reviews, hosted checks and human approvals unchanged.

## Phase 3 checks

python3 -m unittest on tools/test_backlog_sync.py and tools/test_rpi_checks.py run directly with its own exit code recorded (no pipe); git diff --check; frontmatter lines 1-5 diff; non-ASCII scan of added lines; local links in new artifacts. Caches external, no bytecode.
