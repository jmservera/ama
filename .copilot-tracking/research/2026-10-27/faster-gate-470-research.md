---
title: Faster local gate research for issue 470
ms.date: 2026-10-27
---

## Research brief

Focused, internal convergence research for issue #470, requested by the owner.
Audience: maintainers of the exact-commit local gate. Scope: changed-path
selection, bounded independent execution, failed-group resume, receipt scope,
and coordinator policy. No full gate, Azure, secret access, cache/image reuse,
protection changes or automatic issue closure. Trusted evidence root:
`.copilot-tracking/research/2026-10-27/`.

The supplied request explicitly authorizes all four RPI phases and publication
to the named topic branch. Run the loop without interactive phase prompts.
The owner's explicit tooling-tier exception supersedes the older unconditional
full-gate wording for this task.

## Extensions and participation

Repository instructions and RPI phase skills apply. Research is inline because
the uncertainties form one coupled receipt/execution trace. No specialist or
external web research is necessary. Independent critique and Review will be
delegated in their respective phases. No clarification is needed.

## Questions and candidate areas

1. What must selection preserve? Inspect group setup and trusted command matrix.
2. Which mutable resources prevent naive threading? Inspect process tracking,
   editable installs, shared venvs, SQL and image builders.
3. How can resume preserve the exact-commit guarantee? Inspect receipt identity,
   immutable output, environment hashing and live image verification.
4. What timing evidence can honestly be published without a full run?

## Cycle 1

### Wider

Issue #470 and the owner-supplied analysis identify selection and avoided reruns
as the lowest-risk wins. The current runner executes all groups serially and
holds one host-wide lock for the entire run (C1). The supplied analysis measures
17 completed historical full runs at 23-26 minutes; parallel 9-12 minutes and fast
3-8 minutes are estimates, not measured outcomes (W1).

### Deeper

The trusted verifier compares a single global command order, requires every
venv/image/browser artifact and has no scope field (C2). Project installs delete
editable metadata, namespace/static/infra/migration share one venv, and API,
browser and SQL share another. Runner group/process fields and log numbering
are mutable (C3). Naive thread pooling would race all of these.

### Contrarian

Replaying commands from a failed receipt would turn data into executable input.
Accepting a changed HEAD on resume would invalidate previous successful tests.
Dropping failed commands into a passing command stream would violate the
trusted matrix. Therefore resume must use trusted group dispatch, immutable
prior evidence, unchanged identity/tool/environment/file/image inputs, and
separate provenance for reused groups. Partial evidence must never satisfy
default full verification. Fresh image rebuild/scan policy is retained; image
reuse and shared caches are deferred, not silently introduced.

## Evidence log

| ID | Source | Finding |
| --- | --- | --- |
| C1 | tools/rpi-checks.py:1500; tools/rpi-checks.py:1676 | Serial full runner and fixed heavy lock |
| C2 | tools/rpi-checks.py:654; tools/rpi-checks.py:1620 | Ordered schema-3 full-only verifier |
| C3 | tools/rpi-checks.py:825; tools/rpi-checks.py:984; tools/rpi-checks.py:1098 | Shared runner state, editable installs and namespace venv |
| C4 | .github/agents/ama-backlog-delivery-coordinator.agent.md:197 | Stale unconditional full-gate publication requirement |
| W1 | Owner-supplied external gate-speed-analysis-2026-10-27.md, read 2026-10-27 | Historical timing and unmeasured projections |

W1 is the explicitly supplied local session analysis, not a public URL or a
new benchmark. It is not independently remeasured as a full run here.

## Decisions and readiness

Accepted: explicit partial/full scope with default full verification; fail-closed
mapping; serialize shared mutable setup and SQL/image resources; preserve the
single host lock; bound workers by CPU and memory; retain immutable resumed
evidence. Add focused tooling lint/type checks to the small tier rather than
running unrelated Bicep/SQL checks for changes to this tool.

Rejected: arbitrary command replay, receipt promotion across commits, unchecked
partial-as-full verification, cache freshness reductions and full benchmarking
against the owner's explicit prohibition.

Research disposition: executed. Planning Readiness: Ready.
All four questions are covered; remaining uncertainty is implementation/test
behavior, owned by Implement. No second research cycle is indicated.
