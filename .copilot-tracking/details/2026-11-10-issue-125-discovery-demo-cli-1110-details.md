<!-- markdownlint-disable-file -->
# Details: issue 125 fixed synthetic discovery-demo CLI

Plan: [.copilot-tracking/plans/2026-11-10-issue-125-discovery-demo-cli-1110-plan.md](../plans/2026-11-10-issue-125-discovery-demo-cli-1110-plan.md)

## Fixture `zava-synthetic-discovery-demo-v1` (explicitly fictional)

| Event | Property | Stage | Timestamp |
| --- | --- | --- | --- |
| SYN-EVT-001 | SYN-P1 | survey | 2026-03-02T09:00:00+00:00 |
| SYN-EVT-002 | SYN-P1 | design | 2026-03-03T09:00:00+00:00 |
| SYN-EVT-003 | SYN-P1 | install | 2026-03-05T21:00:00+00:00 |
| SYN-EVT-004 | SYN-P1 | handover | 2026-03-06T09:00:00+00:00 |
| SYN-EVT-005 | SYN-P2 | survey | 2026-03-09T10:00:00+01:00 |
| SYN-EVT-006 | SYN-P2 | design | 2026-03-09T21:30:00+00:00 |
| SYN-EVT-007 | SYN-P2 | install | not-recorded (unusable, gap) |

## Hand-derived EXPECTED constants (constructed expectation, not observation)

* survey: P1 24 h + P2 (09:00Z to 21:30Z) 12.5 h = 36.5 h
* design: P1 03-03 09:00 to 03-05 21:00 = 60 h; install: 12 h; handover (final event) and P2 design (last usable) add nothing.
* References: SYN-EVT-001 to SYN-EVT-006 (007 unusable, not referenced).
* Gaps: `unusable-timestamp:SYN-P2/install`.
* Fallback draft (full literal): `design: 60 hours; install: 12 hours; survey: 36.5 hours. Sources: SYN-EVT-001, SYN-EVT-002, SYN-EVT-003, SYN-EVT-004, SYN-EVT-005, SYN-EVT-006.`
* Critique amendments (applied): company connection DENY derives from the readiness report; no-access tests patch open/os.environ/os.getenv and use a poisoned ZF_DATA/empty HOME subprocess.

## P1 module

* `run_demo() -> dict[str, Any]`; `render(report) -> str` (JSON, indent 2, sorted keys); `main(args: Sequence[str]) -> int`.
* Calls: `assess_readiness([])`, `authorise_tool` for fixed names, `calculate_stage_durations`, `draft_evidence(d)` with no drafter, `check_repeatability(_calculate, events, 3)`, `compare_methods([])`.
* `_calculate(events)` is a module-level wrapper returning plain dict so digests are stable; tests patch it for repeatability failure.
* `overall_passed` requires expected match and repeatability identical; `main` prints JSON then exits 1 and writes a reason to stderr on failure.
* No ReadOnlyToolbox, no readiness report manufactured, no file, env, clock or network access.

## P2 dispatch

`__main__`: `argv[1:] == []` or first argument not `discovery-demo` keeps printing the version; `discovery-demo` with any further argument exits 2 with `unknown argument` on stderr.

## P3 tests

Direct module cases plus `subprocess` of `sys.executable -m zava_forward.core` with `cwd` set to a temp dir, clean env (no ZF_DATA, no HOME-based path), asserting the imported package file lies under this worktree.

## P4 README

Append a short paragraph and command to the existing "Discovery assistant readiness and read-only boundary (#125)" section only.
