<!-- markdownlint-disable-file -->
# Plan: issue 125 fixed synthetic discovery-demo CLI

* Task: `125-discovery-demo-cli-1110` / `issue-125-discovery-demo-cli-1110`
* Research: [.copilot-tracking/research/2026-11-10-issue-125-discovery-demo-cli-1110-research.md](../research/2026-11-10-issue-125-discovery-demo-cli-1110-research.md)
* Details: [.copilot-tracking/details/2026-11-10-issue-125-discovery-demo-cli-1110-details.md](../details/2026-11-10-issue-125-discovery-demo-cli-1110-details.md)
* Plan authored (actual tool UTC): between tool UTC 2026-11-10T03:03:31Z and 2026-11-10T03:04:50Z (observed bounds)
* Base: main `a61bebe6b71e7f33560e2dee74b38834e4f55c0e`; local only; `Refs #125` only; correction balance UNKNOWN, no allowance.

## Phases

* [x] P1: Add `discovery_assistant_demo.py` composing the six existing helpers over the fixed fictional fixture with constructed EXPECTED constants.
* [x] P2: Dispatch `discovery-demo` in `__main__.py`; keep no-argument and non-demo behaviour unchanged; unknown demo arguments fail with exit 2.
* [x] P3: Add `tests/test_discovery_assistant_demo.py` (module, mismatch, repeatability failure, fallback, DENY, absent proof, installed-package subprocess, version and argument behaviour).
* [x] P4: Extend only the existing discovery section of `src/core/README.md` with the demo command and its evidence boundary.
* [x] P5: Focused validation: all discovery suites, new tests, installed worktree package via unique venv, ruff check/format, mypy.
* [ ] P6: Commit with repository-local noreply identity; freeze hash/tree; write changes and review records and handoff.

## Out of scope

Dependencies, helper rewrites, APIs, nav, stores, SQL, browser, cloud, Agents, prompts, tools/coordinator evidence, 185 IoT Registry content, push and PR.
