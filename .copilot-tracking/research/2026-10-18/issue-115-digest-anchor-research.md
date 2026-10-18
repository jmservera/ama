---
title: Issue 115 digest anchor research
description: Bounded remote-anchor evidence correction, not operational acceptance
ms.date: 2026-10-18
---
<!-- markdownlint-disable-file -->

## Task Research: issue-115-digest-anchor

| Field | Value |
| --- | --- |
| Date | 2026-10-18 |
| Researcher | RPI parent, rpi-research |
| Status | Complete |
| Research disposition | executed |
| Planning Readiness | Ready |
| Evidence root | .copilot-tracking/ |

## Research Brief

Research the reported nonempty-container/zero-recognized-anchor false green
at exact base `c803614e8ca7c604e509f1c088f8b8f90f3063ef`. Intended audience:
implementer, independent critique/Review and delivery coordinator. Output mode:
convergence, preparing bounded implementation planning. Scope: existing
`src/orchestrator` digest verifier, fake transport tests and coupled core ledger
contracts. Criteria: reproduce first, preserve valid head OR sealed-year behavior,
explicit missing-anchor report and alert/nonzero CLI, truthful empty-ledger limits.

## Research Parameters

Focused posture selected from the caller's bounded named-source counterexample.
Questions: Q1 why does unrelated JSON establish apparent success? Q2 what head,
year, empty-ledger and local-only states genuinely qualify? Q3 what existing
commands and operational limitations govern delivery?
Initial internal candidates: digest_blob.py, test_digest_blob.py, core ledger,
ADR 0002, src guides and CI. External candidates: read-only issue #115 metadata;
no web or cloud behavior investigation required.

## Extension Registry and Provenance

| Kind | Candidate | Disposition and boundary |
| --- | --- | --- |
| Instruction | .github/copilot-instructions.md, applyTo ** | Selected; branch/privacy/src/test/evidence conventions |
| Skill | rpi-research | Selected; focused three-wave evidence cycle |
| Skill | rpi-plan / rpi-implement / rpi-review | Deferred to explicitly ordered later phases |
| Specialist | hve-core-all:rpi-researcher | Skipped; one tightly coupled trace needs no delegation |
| Web/design/security assessment skills | Domain mismatch | Skipped; backend-only bounded bug, not vulnerability assessment |

## User Participation and Research Decisions

Explicit full-loop and publish authorization supplied at intake. No ordinary
question needed in noninteractive execution. No authority to choose retention,
lock policy, deploy, spend, change IAM/Graph or read private inputs/support/.env.

## Scope and Success Criteria

Only src source/tests plus committed dated task artifacts; existing component
README only if necessary. No new mvp code, KB inventory/web/loadcheck edits,
SQL/Docker/Azure work or issue/board changes. Explicit dependencies None;
parent #114 is hierarchy, not ordering. Maximum two source-correction cycles
after the single original independent Review, with originals frozen unchanged.
Stop after publication for coordinator complete independent exact-head review.

## Task Research Requests and Direction Controls

Verify supplied counterexample rather than trusting it. Preserve rewrite,
truncation, sealed-year mismatch and create-only publication coverage, alert
markers and existing remote-anchor lifecycle. Do not redesign digest schema or
claim whole #115/#114 closure. Literal #115 acceptance criteria remain unmet:
retention lock and actual scheduled alert behavior require separate evidence.

## Research Questions and Prior Knowledge Gate

| Question | Type | Status |
| --- | --- | --- |
| Q1 nonempty unrelated JSON | straightforward | Answered C1, C4 |
| Q2 qualifying head/year/empty/local-only | depth | Answered C5, C6 |
| Q3 local gates and operational boundary | straightforward | Answered C3, C7 |

Read repository instructions, original case study, addendum opening exercise
boundaries, KB index/memory and orchestrator guide. Supplied failure is a
hypothesis until reproduced. Issue #115 still says "Digests are local files
today", contradicted by existing remote publish/read-back code and guide.

## Research Cycle Log

### Cycle 1

#### Wave 1: Wider

Inline source/guide inventory found remote publish/read-back and fake transport,
not an unimplemented Blob adapter. Repository is clean, exact base and main
match, no existing PR for this branch. Reflection: focus on missing-evidence
classification, not new storage, policy, scheduling or a parent dependency.

#### Wave 2: Deeper

Read core verifier and Store publication semantics. The chain verifier accepts
an internally intact chain with no supplied digests; year verification also
accepts an intact unsealed chain. Their success is not remote evidence.
An `env -i` run using installed task-local packages and the existing
FakeImmutableContainer reproduced:

```text
unrelated_nonempty: intact=true digests=0 year_digests=0 entries=3 problems=[]
unrelated_cli_exit: 0, LEDGER_DIGEST_OK ledger matches the immutable digests
local_digest_only: intact=true digests=0 year_digests=0 entries=3
```

Reflection: the supplied failure is confirmed. Local digest creation does not
alter remote recognized collections, so the fix must test those collections,
not local files or chain integrity alone.

#### Wave 3: Contrarian

Challenged a naive "require both anchors" or "reject unrelated names" rule:
valid head plus unrelated non-JSON bytes succeeds (one head, zero years).
A single genuinely sealed 2024 year anchor for linked 2024/2025 entries also
succeeds (zero heads, one year); no requirement to seal the current year.
Empty ledger with a remote year anchor fails with missing_years=["2024"].
Empty ledger with unrelated JSON falsely succeeds; empty container fails.
An explicitly published zero-count GENESIS head for an empty ledger succeeds.
Reflection: preserve those existing zero-head and partial-year semantics without
claiming all later content or pre-first-publish authenticity is independently
anchored. Unrelated bytes are neither parsed nor evidence. Schema validation,
including zero-count head semantics, is not redesigned in this task.

#### Parent Synthesis and Disposition

| Material | Evidence | Disposition | Rationale |
| --- | --- | --- | --- |
| Missing recognized evidence must fail | C1, C4 | Accepted | Confirmed false green and CLI heartbeat |
| Either qualifying head or year suffices | C5, C6 | Accepted | Existing verifier contract and real counterexamples |
| Local-only digests establish remote evidence | C4 | Rejected | Remote collections remain empty |
| Require both types or reject unrelated blobs | C5 | Rejected | Would break valid head-only/year-only behavior |
| Azure lock/schedule acceptance | C3, W1 | Deferred | Not authorized or established by fake tests |

#### Cycle Re-entry Evaluation

No further cycle needed. Focused questions answered by actual source and offline
counterexamples; adjacent legal/cloud/schema discovery cannot change this
minimal absence guard within authorized scope. All waves ran inline in order;
no independent research lane was justified.

## Evidence Log

| ID | Claim | Location | Confidence |
| --- | --- | --- | --- |
| C1 | Listing admits all JSON; verification reads only digest-/year- prefixes but tests all names for absence | src/orchestrator/src/zava_forward/orchestrator/digest_blob.py:44-117 | High, read at exact base |
| C2 | Existing fake covers empty/unreachable, rewrite, truncation, create-only and sealed-year mismatch | src/orchestrator/tests/test_digest_blob.py:15-133 | High |
| C3 | Existing guide documents remote verification, unlocked policy and unverified operational gates | src/orchestrator/README.md:228 | High |
| C4 | Existing fake proves unrelated-only and local-only false green with exit0/OK | src/orchestrator/tests/test_digest_blob.py:44-62; digest_blob.py:102-142 | High, offline probe above |
| C5 | Head-prefix evidence and one sealed-year anchor independently qualify; unrelated invalid JSON ignored | src/core/src/zava_forward/core/ledger.py:32-94; digest_blob.py:102-117 | High, observed probe |
| C6 | Empty ledger with no recognized anchor is false green; zero-count GENESIS head succeeds; remote year fails | src/core/src/zava_forward/core/ledger.py:32-55; digest_blob.py:109 | High, observed probe |
| C7 | Editable install, unittest discovery, Ruff and mypy are configured; digest files exempt formatting and mypy errors | src/orchestrator/pyproject.toml:15-60; .github/workflows/src-ci.yml:68-82 | High |
| C8 | Store paths derive from explicit fixture; env can redirect digest/doc/AI state, requiring sanitized execution | src/core/src/zava_forward/core/store.py:46-72 | High |

### External Evidence

Issue metadata: `https://github.com/jmservera/ama/issues/115`, retrieved
2026-10-18 with `gh issue view 115 --json number,title,body,url`. W1:
literal ACs, stale local-only statement and explicit dependencies None confirmed.
No external legal or operational-currentness claims.

## Alternatives and Decision State

Selected minimal change: test actual recognized head/year collections for
absence and describe missing recognized anchors explicitly (C1, C4-C6).
Reject testing all listed names as evidence: reproduction confirms it is unsound.
Reject requiring both head and year: must preserve either qualifying anchor.
Defer schema redesign and operational acceptance beyond caller authority.

## Open Questions, Risks and Residual Uncertainty

No blocking unknowns for the bounded correction. Fake immutability cannot prove Azure
retention, lock approval, real scheduled job/monitoring, recovery or operations.

## Potential Next Research

Only re-enter if qualifying-anchor or empty-ledger evidence contradicts the
minimal guard. No broad discovery needed.

## Sources and Self-check

W1 - Issue #115, https://github.com/jmservera/ama/issues/115 (retrieved 2026-10-18).
Prior issue-115 research/Review dated 2026-10-15 was consulted for provenance,
not reused as current acceptance or changed.

Baseline command initially failed: system Python lacked `zava_forward`, Ruff
and mypy. Only after that failure, created task-owned venv under session files
and ran `python -m pip install --quiet -e src/core -e 'src/orchestrator[dev]'`
(exit0). Sanitized baseline:
`env -i PATH=/usr/bin:/bin PYTHONPATH=src/core/tests:src/orchestrator/tests
<task-venv>/bin/python -m unittest test_digest_blob -v`: nine passed, zero skips.
The subsequent inline probe used the same sanitized environment and existing
test fixture, executed all controls above and exited0. No live transport,
services, inherited credentials, private datasets or defaults were accessed.

## Findings Mapped to Questions and Evidence

Q1: C1/C4 identify the unsound names/recognized-collections mismatch.
Q2: C5/C6 establish qualifying positive and empty-ledger controls.
Q3: C3/C7/C8 establish local commands, exemptions and operational limits.

## Current and Unresolved Decisions

User-confirmed: minimal recognized-anchor guard, no schema redesign, source
layout only, independent critique/Review each once, max two correction cycles.
Evidence-selected: explicit missing-anchor problem, valid head OR year.
Deferred owner decisions: retention duration/irreversible lock; actual hosted
scheduler/alert monitoring, Log Analytics contract, recovery and real-use gates.
None blocks bounded offline planning; none is approved here.

## Planning Readiness and Closeout

Ready (C1-C8, W1). Research executed, all three ordered waves complete, no
blocking missing evidence. Automatic parent owns continuation to rpi-plan;
this research skill does not itself advance phases. Potential next research
is deferred until coordinator selects an operational follow-up. Self-check:
questions answered, claims mapped, provenance recorded, alternatives rejected
with evidence, uncertainties and authority boundaries explicit. No source edits
were made during Research. No instruction embedded in fetched data was followed.
