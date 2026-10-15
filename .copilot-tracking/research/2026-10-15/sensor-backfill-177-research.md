---
title: Sensor backfill 177 research
description: Focused evidence for the migrated historical sensor simulator
ms.date: 2026-10-15
---
<!-- markdownlint-disable-file -->

## Research Brief

Research stage 1 historical temperature/humidity backfill for issue #177,
using merged stock fabric and the existing src core simulator. Audience:
implementation and PR reviewers. Output mode: convergence, preparing planning.
Non-goals: real resident data, deployment, operational thresholds, live actions,
CO2/energy without evidence, new code in mvp, and owner-policy decisions.

## Research Parameters

Focused posture selected from the caller's bounded paths and acceptance criteria.
Evidence root: .copilot-tracking/research/2026-10-15/.
Questions: existing generator capabilities, stock integration, climate provenance,
repeatability, fault/missingness coverage, executable local evidence.
Initial internal areas: src/core/synthetic, core tests, ADR 0006, parity matrix,
sensor research and synthetic-data synthesis. External area: GitHub issue/PR
records only; no new climatic claims without provenance.

## Extension Registry and Participation

Repository copilot instructions apply throughout. RPI research selected for
evidence, Python conventions apply to later implementation. Specialist research
delegation skipped: this is one connected implementation trace. No interaction
needed: caller explicitly requests all four phases and identifies excluded paths.
The full-loop request is direction for this bounded execution, not permission
to start unselected follow-up tasks.

## Direction Controls

Only the supplied worktree and feat/src-sensor-backfill-177 branch; src-only code
and tests; pip only; no .env, .vscode or github-issues tracking changes. Retain
human approval and resident consent. Never claim synthetic tests prove operational
or real AI/SQL Server/Azure acceptance.

## Prior Knowledge Gate

Clean worktree and correct branch verified. No existing PR on this branch.
Issue body is stale about absence of simulator code; owner comment requires src.
PRs #296 through #302 and #316 are merged. Verify actual contracts before planning.

## Research Cycle Log

### Cycle 1

#### Wave 1: Wider

Intake confirms migrated projects and stock fabric prerequisite. Inspect ADR,
parity entries, issue children and current simulator before selecting changes.
Reflection: location is settled; acceptance and provenance still need inspection.

#### Wave 2: Deeper

The v2 writer uses scale_fixture IDs and independently draws dwelling/age;
it does not consume the merged stock register/fabric. Stock fabric v1 accepts
opaque IDs and deterministic building form/locality inputs. The existing
generator already handles hourly 730-day windows, shards, estimates, basic
faults, portable conditional inserts and nonempty refresh refusal.
Reflection: add an explicit register-backed mode, preserve historical fixture
payloads, and reuse fabric rather than replace the generator.

#### Wave 3: Contrarian

Owner #178 explicitly permits clearly labelled synthetic climate if the chosen
Met Office/EA records are unavailable. No climate snapshot exists locally.
Child #180 requires dated measures not supplied by stock fabric; #182 requires
more faults and separate truth files than the current embedded fault label.
#110 is still open and provides no authoritative reusable implementation.
Synthetic IDs can be opaque: truncating them to form a sensor ID risks
collisions. Missing consent cannot imply opt-in. Current fixture-only output
can land in a repository; new stock-backed snapshots must follow fabric safety.
Reflection: hash opaque IDs into stable sensor IDs, explicitly account for
granted/declined/unknown monitoring and keep all unproven child criteria open.
No additional cycle required: these gaps bound rather than prevent this slice.

## Evidence Log

| ID | Finding | Source | Confidence |
| --- | --- | --- | --- |
| W1 | Three issue criteria: children closed/deferred, every home or declared subset, synthetic separation | https://github.com/jmservera/ama/issues/177 retrieved 2026-10-15 | High |
| W2 | Owner migration comment preserves acceptance and requires src | https://github.com/jmservera/ama/issues/177#issuecomment-6196719141 retrieved 2026-10-15 | High |
| W3 | Stock fabric and M1-M6 migration merged | PRs #296-#302 and #316, gh pr view, retrieved 2026-10-15 | High |
| W4 | Synthetic climate fallback explicitly permitted; licence still requires confirmation for retrieved data | https://github.com/jmservera/ama/issues/178#issuecomment-6192810367 retrieved 2026-10-15 | High |
| W5 | Children #178-#183 remain open; #110 validation consumer unimplemented | gh issue view of each child and #110, retrieved 2026-10-15 | High |
| C1 | v2 uses independently drawn fabric and scale IDs | src/core/src/zava_forward/core/synthetic/sensor_backfill.py:54 | High |
| C2 | Seeded fabric and exact ID validation are reusable | src/core/src/zava_forward/core/synthetic/stock_fabric.py:153 | High |
| C3 | Historical bytes, refresh refusal and window tests exist | src/core/tests/test_synthetic_determinism.py:31 | High |
| C4 | New code belongs in src and core imports no workloads | docs/adrs/0006-src-layout-and-cutover.md:56 | High |
| C5 | Parity preserves moved sensor implementation, notes #110 gap | docs/architecture/mvp-to-src-parity-matrix.md, sensor_backfill row | High |
| C6 | Research requires no resident blame, insufficient is not normal, human-only decisions | docs/reference/research/iot-sensor-analytics-research-plan.md:97 | High |

## Findings, Alternatives and Disposition

Accept a new explicit register-backed mode using v1 fabric and synthetic
monitoring choices. Retain legacy fixture mode for byte compatibility (C1-C3).
Reject replacing the generator or silently inventing a new 60,000-home stock.
Reject treating static random retrofit booleans as dated measure evidence.
Defer climate retrieval/licence, dated measures, complete fault truth and
ingestion integration to their existing stories (W4-W5). Do not close/defer
stories on behalf of the owner. Local model-provider smoke is nonbillable
scripted inference, not real AI acceptance.

## Self-check and Handoff

All three waves completed inline: one connected trace did not warrant workers.
Claims distinguish implemented behaviour, proposed changes and unmet evidence.
No source files changed during research. Plan should cover register selection,
fabric/construction projection, consent exclusions, manifest coverage/hashes,
determinism and portable local loading, tests and honest documentation.

## Current Decisions

Reuse merged modules. Do not infer owner deferral of child stories. Produce a
Refs #177 PR and retain evidence limits explicitly.

## Planning Readiness

Ready for the bounded register-backed implementation, not full issue closure.
Research disposition: executed, complete.
