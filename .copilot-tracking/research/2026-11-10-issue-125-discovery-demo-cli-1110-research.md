<!-- markdownlint-disable-file -->
# Research: issue 125 fixed synthetic discovery-demo CLI (initial composition)

* Opened (prospective, actual tool UTC): 2026-11-10T03:03:09Z
* Branch: `feat/synthetic-discovery-cli-125-1110`; worktree `/home/azureuser/source/ama-demo-wt/issue-125-discovery-1110`
* Base/target: main `a61bebe6b71e7f33560e2dee74b38834e4f55c0e` (tree `a54ed33ac56ca2a29a5fcf7f551c70f84d96bd10`)
* Mode: manual-sequenced full loop run in order by owner direction; Research disposition: `executed`.
* Scope: LOCAL ONLY, no push, no PR. This is a NEW initial remaining composition, not a renamed correction. Historical correction balance is UNKNOWN; no reset or post-independent-review correction allowance is granted and none is inferred from r5/r6 names.

## Sources read

* Case original and addendum, `docs/reference/README.md`, `docs/reference/memory.md`, `src/core/README.md` discovery section (line 1070 onward), `docs/brds/retrofit-flow-discovery-brief.md`.
* Authoritative refinement (external, session folder `discovery-125-demo-refinement-1110.md`) and its appended history reconciliation. Its original hold opinion is preserved; the reconciliation resolved it.
* Delivered helpers (reviewed, not this CLI): 894 `discovery_assistant_boundary`, 1033 `discovery_assistant_evaluation`, 1161 `discovery_assistant_drafting`.
* `src/core/src/zava_forward/core/__main__.py` (prints `zava-forward-core {version}`, ignores arguments).

## Findings

* Helpers exist and are pure: `assess_readiness`, `authorise_tool`, `ReadOnlyToolbox` (requires a ready report), `calculate_stage_durations`, `draft_evidence(durations, drafter=None)`, `compare_methods`, `check_repeatability`.
* Missing: one composition exercising them together over a fixed explicitly fictional fixture, reachable by a credential-free installed-Core command.
* `ReadOnlyToolbox` cannot be instantiated without a READY report; the demo must not manufacture one. It therefore uses `authorise_tool` decisions only (policy denial prevents dispatch; no tool callable is registered or run).
* `calculate_stage_durations` only treats timezone-less/unparsable timestamps and blank source references as gaps; the final event of a property adds no duration (incomplete final stage).
* `MANUAL_PATH` and `compare_methods([])` leave `criterion_met=False`, `incomplete` for all ten measures.
* No documented version invocation exists beyond running `python -m zava_forward.core` with no arguments; behaviour must stay unchanged for it and for any non-`discovery-demo` argv.

## Boundaries and constraints

* Allowed functional files: `__main__.py`, new `discovery_assistant_demo.py`, new `tests/test_discovery_assistant_demo.py`, existing discovery README section. No dependencies, helper rewrites, APIs, stores, SQL, browser, cloud, Agents, prompts.
* Overlap: 185 c7cf owns a new IoT Registry module and a different Core README section (shared README filename acknowledged; edits kept local to the discovery section, 185 content not copied); 1300 owns tools/coordinator phase evidence; 132/133 reserve shared intake/hooks; 1296/146 paused.
* Phase 0 gates operational company connection, not this expressly permitted synthetic design hypothesis; Phase 0, 123, privacy, access and human approvals are preserved and every whole-125 criterion stays unproven.
* Eventual PR must use `Refs #125`, never a closing keyword.

## Design decisions

* One module, `discovery_assistant_demo.run_demo() -> dict` plus `render()`/`main(argv)`; deterministic JSON (sorted keys, indent 2), no clock, env, filesystem, network.
* Fixture `zava-synthetic-discovery-demo-v1`: two fictional properties (`SYN-P1`, `SYN-P2`), IDs `SYN-EVT-*`, UTC and offset-aware events, one property with an incomplete final stage, one timestamp-less event as a gap.
* Independently authored EXPECTED constants (hand-computed hours, references, gaps) compared with the calculation; mismatch or repeatability failure exits non-zero. These are constructed expectations, not analyst observations.
* Conventional table derived from the same calculation (stated explicitly; not an independent BI engine).
* Comparison matrix from `compare_methods([])`; human comparator pointers empty; no fabricated participants, effort, preference or approval.
* Fallback text is reported with `model_used=false`, never presented as AI output.

## Planning Readiness

Ready.

## Follow-ups (candidate, not yet ranked)

* Independent exact-head assessment before any publication.
* Remaining whole-125 criteria (human evidence, Phase 0 approvals) are not addressed here.
