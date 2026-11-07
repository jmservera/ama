<!-- markdownlint-disable-file -->
# Research 004 (activity handoff for #1207), issue 1204

Addendum on frozen head f381625. Earlier research, critiques and proxy results stand unchanged.

## Disposition

Executed, bounded. Read: AMA repository instructions, `docs/case_study_48_original.md` and addendum, `docs/reference/README.md`, `docs/reference/memory.md` (no edit), the coordinator agent file and the #1207 issue body.

## Evidence

* Coordinator reconcile paragraph ran `backlog-sync.py` then `--apply` with no activity input. #1207 (2026-11-05): legacy `--apply` demoted live rpi-79, rpi-80, rpi-82 to Todo.
* `origin/main` ead177ef9 `tools/backlog-sync.py --help` lists only `--apply`; this branch is identical. The `--active` and `--inactive` flags exist only in the independently inspected candidate `issue-1207-live-state` clean head 6a1326ad6dbb39ca559e9cf124f689e7fcf60790 (reported: 11 backlog and 19 CI tests, ruff, mypy, actionlint passed against ead177ef). Not published or accepted.
* Candidate semantics: `--active` is positive evidence only; `--inactive` only for confirmed open issues with no session and no frozen candidate; otherwise activity is Unknown, status kept and reported unverified.

## Planning Readiness

Ready. Constraint: instruction wording only; no tool, test, application, protection, cloud or memory change.

## Not changed or claimed

Native HVE final intended-profile independent design, execution and grading remains incomplete: authorization for GPT-5.6 Sol was asked but not obtained. No substitute model is specified and no High-profile Pass is claimed. This blocks the behavioral publication lane, not this source repair.
