<!-- markdownlint-disable-file -->
# Research: issue #81 parent alignment (2026-11-06)

Task `81-alignment`, slug `issue-81-alignment`. Research disposition: `executed`.
Planning Readiness: `Ready` for an alignment-only RPI. Not FULL validation,
publication or acceptance.

## Scope and authority

Coordinator-approved bounded work only: rebase this run-adopted parent branch
locally onto freshly fetched `origin/main`, prove preservation of the three
merged child contributions, record a bounded checkpoint, run only no-service
regressions. No new feature, no push, PR, issue write or merge, no FULL gate.
Tier for eventual integrated publication stays FULL.

## Actual observed state (read-only, before any change)

| Item | Value |
| --- | --- |
| Worktree / branch | `/home/azureuser/source/ama-wt/parent-81`, `feat/controlled-lifecycle-integration-81` |
| Starting HEAD (retained identity) | `af891a5cccf730ccf61e670f312b7674218dbe4b` |
| Status at start | clean, ignored-inclusive output empty; `.copilot-tracking/` dated dirs for 2026-11-06 created by this run |
| Freshly fetched `origin/main` (pin) | `56eec736906774ef56d8c9a66ed7f3f9c1e520c6` (#1236, equals the last observation) |
| Merge base before alignment | `bb3a3b03cb94eef6c06ae4b12d07cfe7bbdef43f` (old stack base; the stale bb3a is not used as a workaround) |
| Parent-only commits | exactly three: `cd271cfa5` (#1226), `d4d33c7ec` (#1228), `af891a5cc` (#1229) |
| Main-only commits since base | one: `56eec7369` (#1236), touching `.github/agents/ama-backlog-delivery-coordinator.agent.md` plus `.copilot-tracking` records only; no `src/`, `docs/` or `tools/` change |
| Dry-run `git merge-tree --write-tree origin/main HEAD` | clean, tree `2c0381ecaf3d672ff6b0113df94b2d2ebeb1873c`; no conflict predicted |
| Scratch | `/mnt/ama-gates/restart-1106-81-integration` created (did not exist) |
| Prior native child86 full gate | refused before groups because main `56e` is not a descendant of the old stack (coordinator report; no receipt exists) |

## The three merged contributions (parent-topic observations)

None is merged-main acceptance. Each was a merged child PR into this parent topic.

| PR / commit | Behavior | Source files | Tests |
| --- | --- | --- | --- |
| #1226 `cd271cfa5` | fail-closed quality evidence gate, malformed-metadata and corrupted-replacement handling | `gates.py`, `quality.py`, `store.py` | `test_gates.py`, `test_hazard_referral.py`, `test_quality_procurement.py` |
| #1228 `d4d33c7ec` | quality gate rule provenance qualified to PRD FR-008 | `gates.py` (5 lines) | `test_gates.py` (4 lines) |
| #1229 `af891a5cc` | explicit capacity booking Pass/Fail/Unknown outcomes | `appointments.py`, `gates.py`, `procurement.py` | `test_quality_procurement.py` |

Pre-alignment blob identities at `af891a5cc` (to be compared after rebase):

| Path | Blob |
| --- | --- |
| `src/core/src/zava_forward/core/gates.py` | `0d8d3d15b6e1ce674e257bf19f074a1e7d86cad7` |
| `src/core/src/zava_forward/core/quality.py` | `4a1e299139e85d7ff9d92c342fb4efba608643ec` |
| `src/core/src/zava_forward/core/store.py` | `86948572acce016232286cfc9463702cfeefdf54` |
| `src/core/src/zava_forward/core/appointments.py` | `9dc02c5ab2aa4a081c7bfdba28f3c3c1d9d88ea6` |
| `src/core/src/zava_forward/core/procurement.py` | `f01786666894a54b7016f35bfd23c8c12662d65c` |
| `src/core/tests/test_gates.py` | `91330fb9fcfb40b672641983e2ab7f20547dde69` |
| `src/core/tests/test_hazard_referral.py` | `c89f89f2fb17014f14d61fc6ef30f2a7f1b675ac` |
| `src/core/tests/test_quality_procurement.py` | `7481378934cb140ae53f5871b8e0bfeb880022df` |

Their original RPI evidence (dated 2026-11-05 and 2026-11-06 research, plan,
details, changes and review files for issue-82 slugs) is committed in the
parent history and must survive unchanged. The #1226 state file records an
unrun full gate blocked by the heavy lock; that adverse evidence stays as is.
Original follow-up rank 1 (replacement route for in-progress quality records
with missing evidence) remains an open adverse/gap item, not resolved here.

## Document identities and requirement qualification

| Document | Version / status | Blob |
| --- | --- | --- |
| [BRD](../../../docs/brds/agentic-retrofit-programme-brd.md) | 0.21.0, `draft` | `34d88395de861e9799eb9e24121a21c92c7a5adc` |
| [PRD zava-forward](../../../docs/prds/zava-forward-retrofit-programme-demonstrator.md) | 0.21.0, `in-review`, `author-complete-unsigned-pending-review-and-owner-acceptance` | `c788b917bafaede215f326f0efc71e071a687f1c` |
| [PRD proper-warm](../../../docs/prds/proper-warm-retrofit-programme-demonstrator.md) | 0.13.0, `in-review` candidate, not cited by gate code | `f7f9b7675e60e49006127a374e1106ff18aae282` |
| ADR 0001 to 0007 | blobs `d42fa5c4615f`, `cbe21530043f`, `d60645397b20`, `9406c2e747ce`, `4d610335a5a1`, `956da1a3b804`, `abb21088a9bb` (12 hex prefixes); only ADR 0002 states an owner acceptance line (2026-10-24, staff identity); statuses of others not re-assessed | n/a |

Requirement numbering differs between BRD and PRD and must not be conflated:

| ID | PRD (zava-forward) meaning | BRD meaning |
| --- | --- | --- |
| FR-008 | deterministic evidence, eligibility, authority, safety, resident, funding, capacity, quality and finance gates before a controlled transition (AC-010, AC-011, AC-067, AC-144) | material change invalidates affected downstream approvals (BR-008, AC-011) |
| FR-016 | provider-package record with committed capacity evidence; readiness governed by PRD FR-008 | different topic |
| FR-017 | independent per-measure quality-disposition record; consequential gates governed by PRD FR-008 (AC-020, AC-042) | handoff content (BR-018, AC-023); not quality |

Correct qualification for the gate code: the quality and capacity gates trace to
**PRD FR-008 (governing) with PRD FR-017 (quality) and PRD FR-016 (capacity)**,
and to **BRD RULE-001/RULE-002** (cited by `_BRD` rule sources). **BRD FR-008
is a related but different requirement** (downstream approval invalidation) and
BRD FR-017 must not be cited for quality. `gates.py` already cites the
zava-forward PRD path, which exists at this head; no code change is indicated.
Both documents are draft or in-review; this research does not approve them, and
exercise-fixture rule records stay `_UNREVIEWED` (no legal, operational,
resident or human approval is inferred).

## Component and policy reading

Case study original and addendum, `docs/reference/README.md` index, `memory.md`
(context only), `src/README.md` local-RPI-gate section (FULL requires Python
3.12, Node, Docker, Azure CLI, actionlint, ShellCheck, Trivy; not admitted
here), `src/core/README.md` test invocations (`PYTHONPATH=src:tests python3 -m
unittest <module> -q`) and the tracking retention policy (preserve original and
adverse RPI evidence; no deletion; heavy output to external scratch) were
consulted. Prior checkpoint format taken from the fourth local stabilization
checkpoint in `docs/architecture/cutover-evidence-pack.md` (Refs #440).

## Constraints and unknowns

* The capacity checkpoint consumed at issue #440 comment 6676325240 did not satisfy integrated-parent FULL or epic acceptance.
* Unknown: whether a later stack-tip full receipt is acceptable for the parent member; depends on canonical runner semantics and independent verification, not assumed.
* Unknown: independent, hosted and human approvals; resident, legal and professional approval not established.

## Selected approach

Local rebase of the three parent commits onto pinned main (predicted clean),
preservation proof via blob comparison and `git range-diff`, focused no-service
tests in an isolated scratch venv, one bounded checkpoint section.
