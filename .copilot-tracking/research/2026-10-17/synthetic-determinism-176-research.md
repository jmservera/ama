---
title: Issue 176 recovery research
description: Fresh verification of PR 368 without reconstructed ephemeral logs
ms.date: 2026-10-17
---

## Research Brief and Parameters

Task ID 176; stable slug `synthetic-determinism-176`. Output mode: audit.
Focused posture, selected from the caller's bounded recovery request.
Audience: PR #368 coordinator. Evidence root: `.copilot-tracking/`.
Verify current issue criteria, reviewed head, upstream drift and durable
artifacts before plan verification, implementation inspection and Review.
Prior execution claims are historical reports, not execution performed now.
No lost `/tmp` log will be reconstructed or represented as recovered.

## Extensions, Participation and Direction Controls

Repository instructions and rpi-research selected for artifact/evidence rules.
Existing 2026-10-16 artifacts are inputs, not authority to invent validation.
Research is inline because the scope is tightly coupled; no workers launched.
UI, cloud and legal research skills skipped as outside scope. User explicitly
requests all four phases in order and a stop after publication; no automatic
follow-up session or mode change is inferred. No clarification is necessary.
No private datasets, original-register substitute, Azure, spending, secrets,
primary `.env`/`.vscode`, application changes without a genuine bug, merges
or force-pushes. Clean worktree and expected branch confirmed at intake.

## Prior Knowledge Gate and Questions

Read original case study, addendum context, reference index and owner memory.
Read 2026-10-16 research, plan, critique, changes, Review and state.
Q1: Do current issue/PR facts support the supplied claims?
Q2: What changed on main relative to the reviewed branch and review time?
Q3: Which acceptance boundaries and validation obligations remain?

## Research Cycle 1

### Wider

Current issue and PR retrieved through `gh`; expected head is
`196972dc0dac256cdfd41f70bc06e7cad5fbebf2`. Issue still OPEN.
PR OPEN, same branch, targeting main, twelve completed SUCCESS checks.
Reflection: historical checks are remotely observable, but are not fresh
local execution. GitHub formal reviews are empty; independent MERGE evidence
needs its actual source and cannot be inferred from that API field.

### Deeper

Read the issue's three current unchecked criteria against the existing plan,
critique PC-001/002, changes and Review RV-001/002. Their partial-acceptance
boundary agrees with the current PR body (W1/W2, C1-C4).
`git merge-base HEAD origin/main` returns
`4ca6c7318ee4be35cef8c5ea6eee3425bf1421c4`, equal to fetched main and PR base.
`git log --first-parent HEAD..origin/main` and
`git diff --name-status HEAD...origin/main` both produce no output.
Reflection: there are no unincorporated main commits at recovery intake.
Neither local recovery nor new CI can retroactively prove lost execution.

### Contrarian

Challenged the literal "main merges since review only changed docs/index/log"
claim. The final pre-recovery merge `196972d` itself contains #175 source and
test additions (`synthetic/privacy.py`, `test_synthetic_provenance.py`,
`src/agents/tests/test_chat_provenance.py`), plus documentation/tracking.
The preceding merge `1a1d88c` contains climate documentation/tracking, including
`src/core/README.md`, not only the reference index/log. Therefore a blanket
docs-only characterization of those historical merges is false. These
changes are already incorporated in the claimed reviewed head, not new
post-head drift. Diffing `f822bb9..196972d` for the feature source, feature
tests, core pyproject and source CI gives no changes. Diffing `196972d`
against main for the #175 core source/tests also gives no changes.

The current GitHub PR has no formal reviews or comments. A targeted search
of durable tracking artifacts and available seven-day session metadata found
no independent MERGE review receipt for this exact head. Treat the supplied
independent MERGE decision as caller-reported, not independently recovered.
The 2026-10-16 inline RPI Review says Complete / Residual work, not MERGE.
The twelve SUCCESS checks are independently verified through the commit
check-runs API, each bound to the exact full head SHA (W3).

Tracked generator-path inventory supports the documented absence of the
original OSM-backed stock-register generator. Only filenames were listed;
no private stock/manifest/geography contents were opened. Before approving
test execution, inspected the four requested modules: they construct
fictional sources/temporary outputs, and the programme builder's
`load_register` is patched with constructed records (C5-C7).
Reflection: these are decisive counterexamples to overclaiming full
acceptance or recovered independent approval, not newly found source bugs.

## Evidence Log

| ID | Finding | Location or retrieved source |
| --- | --- | --- |
| C1 | Existing research preserves absent original generator | `.copilot-tracking/research/2026-10-16/synthetic-determinism-176-research.md:48` |
| C2 | Plan and critique require strict dates, raw hashes, compatibility and finding disposition | `.copilot-tracking/plans/2026-10-16/synthetic-determinism-176-plan.md:92`; `.copilot-tracking/plans/2026-10-16/synthetic-determinism-176-critique.md:93` |
| C3 | Historical execution reports, not new execution | `.copilot-tracking/changes/2026-10-16/synthetic-determinism-176-changes.md:28` |
| C4 | Existing Review retains RV-001/002 | `.copilot-tracking/reviews/logs/2026-10-16/synthetic-determinism-176-review.md:80` |
| C5 | Builder tests substitute fictional register | `src/core/tests/test_generated_dataset.py:46` |
| C6 | Fabric and sensor repeatability run on constructed/temporary sources | `src/core/tests/test_synthetic_determinism.py:35`; `src/core/tests/test_sensor_stock.py:138` |
| C7 | Published audit explicitly retains all acceptance boundaries | `docs/reference/research/retrofit-synthetic-data/README.md:220` |
| C8 | CI project lint/type commands | `.github/workflows/src-ci.yml:84`; `src/core/pyproject.toml:17` |
| W1 | Current issue OPEN; all three criteria unchecked | https://github.com/jmservera/ama/issues/176, retrieved 2026-10-17 via `gh issue view 176 --json title,body,state,url` |
| W2 | Current PR head/base/body, empty formal reviews/comments and no closing relationships | https://github.com/jmservera/ama/pull/368, retrieved 2026-10-17 via `gh pr view 368 --json ...` |
| W3 | Twelve successful exact-head check runs | https://api.github.com/repos/jmservera/ama/commits/196972dc0dac256cdfd41f70bc06e7cad5fbebf2/check-runs, retrieved 2026-10-17 via `gh api` |

## Synthesis, Alternatives and Decisions

Accepted: use existing artifacts as historical inputs, rerun scoped tests and
whole-core project lint/type checks, publish fresh dated artifacts only.
Rejected: reconstructing lost logs, inventing a recovered MERGE receipt,
calling all historical merges docs-only, or manufacturing original stock.
Deferred: original source/input/runtime recovery and human policy adoption.
No further research cycle is warranted: the remaining evidence is unavailable
or outside authorized access, rather than resolvable by more source search.

## Acceptance Mapping and Residual Uncertainty

| Criterion | Recovery research result |
| --- | --- |
| AC1 every generator including original stock/sensors | Unmet overall; available generator replay remains conditional on constructed inputs/runtime. |
| AC2 seed/version/revision manifests | Partial overall; historical manifests unchanged and original generator cannot issue a new receipt. |
| AC3 refresh cadence, approvals, live protection | Met as documentation only; no owner policy adoption or live reset authority. |

No lost historical local run is attested. No original stock reproduction,
full-stock sensor execution, cloud acceptance or human approval is inferred.
An initial `gh pr view --comments --json` combination failed because the CLI
allows only one; corrected to `--json comments,...` and retrieved successfully.
No source mutation resulted.

## Disposition and Readiness

Research disposition: executed, Complete. Planning Readiness: Ready for
bounded recovery verification, not full issue acceptance. Self-check: all
three waves performed inline in order; material claims have source/tool
provenance; missing evidence and caller controls remain explicit.
Continuation: user-directed RPI parent proceeds to Plan verification.
