<!-- markdownlint-disable-file -->
# Changes 003 (C1-C3 correction), issue 1204

Addendum after head 04ed9a8. Earlier commits and evidence are preserved.

## Original adverse result recorded

A new independent exact-source static review of 04ed9a8 found three High contradictions: C1 (CI-economy bullet allowed merge at once after an append-only docs rebase on old-head green evidence), C2 (step 5 told the worker loop to push artifacts, against the worker-publication prohibition), C3 (16-20 open PRs "launch nothing" also barred existing-PR repair and review continuations). That review's own file was supplied by the coordinator and is summarised here; this record does not replace it. The 04ed9a8 commit and its prior Pass claims are therefore superseded for these three clauses.

## Source change (`.github/agents/ama-backlog-delivery-coordinator.agent.md`, frontmatter unchanged)

* C1: merge-at-once removed; a docs rebase needs step 7/8 exact-head evidence, assessment and hosted checks.
* C2: missing RPI artifacts go back as a frozen local correction; coordinator alone verifies, assesses and publishes.
* C3: 16-20 and above 20 bar new issue admissions only; existing-PR repair, correction and review continuations stay within the eight-live-session cap; drain to 10-15 kept.
* Grade-003 M1 and M2: step 7 verdict bound to the exact head; step 8 assesses the rebased head before the force-with-lease push.

## Stages

* Authoring: separate subagent for C1-C3; M1 and M2 small edits by the lead (disclosed deviation).
* Static closure: independent reviewer (`-review-003.md`) Pass for C1-C3 and for M1/M2.
* Behavior: T1-T3 executors, independent grader (`-behavior-grade-003.md`: Pass with M1, M2 Medium, fixed afterwards), T1 rerun on the final text. Proxy model unknown, lead-designed scenarios, emulated commands, single runs. The earlier lead-graded R1/R5/R6 run stays lead-graded; no independent grade of it exists, so no clean HVE claim is made for that run.
* Not claimed: runtime guarantee, historical grades as new exact-head execution.

## Validation

* Deferred: focused `rpi-checks.py --changed` receipt. A full gate (#188) holds `/tmp/ama-rpi-heavy.lock` (holder PID 1148896); run later with `--lock-timeout 0` once free, never queue. `/tmp/rpi1204-corr-focused-1152746` is preserved as incomplete adverse evidence. The ef585f5 receipt does not validate any later commit.
* Run at the final head: `git diff --check`, frontmatter, ASCII and local-link checks (results in the final report).
