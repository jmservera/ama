<!-- markdownlint-disable-file -->
# Changes 004 (activity handoff for #1207), issue 1204

Addendum after head f381625. Earlier commits, critiques, proxy results and the C1-C3/M1-M2 fixes are preserved.

## Source change

`.github/agents/ama-backlog-delivery-coordinator.agent.md` (frontmatter unchanged):

* Reconcile paragraph: check `--help` before using `--active`/`--inactive`; do not run legacy `--apply` until the #1207 tool change is accepted and published; `--active` is positive evidence only; `--inactive` only for individually confirmed open issues with no session and no frozen candidate; unknown activity stays explicit and is not a global stop; board readback and closure/human gates retained.
* Recurring schedules: delivery prompts carry this handoff.

## Not changed

Tool code, tests, application code, protection, cloud configuration, repository memory. No heavy receipt.

## Commands and results

* `python3 tools/backlog-sync.py --help` here and on `origin/main` (ead177ef9): only `--apply` (flags unsupported, so no apply was executed).
* Candidate `issue-1207-live-state` clean at 6a1326ad: `--help` lists `--active` and `--inactive`.
* `git diff --check`: clean. Non-ASCII grep of the agent file: none. Diff touches only the two intended places.

## Open

* Native HVE final intended-profile independent design/execution/grading incomplete: GPT-5.6 Sol authorization asked, not obtained. No substitute model; no High-profile Pass. Blocks the behavioral publication lane only.
* Focused `rpi-checks.py --changed`, independent exact-head assessment, hosted checks and owner approval remain with the coordinator.
