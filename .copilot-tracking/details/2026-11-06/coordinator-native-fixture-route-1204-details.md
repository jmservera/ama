---
title: Details for a contained native fixture route (issue 1204)
ms.date: 2026-11-06
---

## Containment proof requirements (all before any model call)

1. Source fingerprint: agent copy blob equals acefb44a4d254ede6d86413343127b763dec42cb before and after; the copy is the only agent resolved (strace on that path as in earlier runs, or equivalent).
2. Tool surface: record the exact tool list the CLI exposes under the planned `--available-tools`; assert it contains only read tools and the fixture MCP tools. Any shell, edit, create, delegation, schedule or fetch tool present is a stop.
3. Enforcement independent of the model: an attempted call to a removed tool must fail without side effect, shown by a harmless probe that does not use real resources. If this needs a model call, it needs its own admission.
4. Fixture backend: reviewed source hash; writes only to a per-run external state file; no network, no subprocess, no environment reads; every call (name, arguments, result, order) appended to a raw log; state and log hashes before and after.
5. Credentials: no `.env`, token file or environment dump read; the model-call credential path documented without values; `--secret-env-vars` and `--deny-url` set; confirm no fixture or log contains secret patterns (names-only check).
6. Hooks: not relied on unless coverage of every tool is shown; if used, fail-closed behavior must be demonstrated, since empty output falls to default.
7. Workspace status before and after is identical; scratch directory unique and external; no push, PR, issue, schedule or cleanup.

## Profile and fidelity

* `--model auto`, actual model recorded per run, canonical map unresolved, no tier equivalence claim, no weaker substitute.
* Labels: observed native (agent load, routing, tool-call choice, arguments), fixture-emulated (effects), not tested (production backends, live approvals, resident and legal boundaries).

## Scope of a future batch

Full run only. A fresh generic designer returns content only; the lead writes files. Scenarios cover the 1204 requirements at fixture-action level: liveness and no-op stop, cap of eight active sessions, parent stacking, publication before validation, approval expiry, revocation and fresh quantified approval routing, proof-absent release, cleanup finite selection, Unknown classification, and human and legal boundaries. Expectations are frozen before execution; executor receives only the wrapper, the black-box scenario and non-answer containment. Independent grader returns content only.

## Not authorized

Any dependency install, hook or harness creation, sandbox enablement, nested CLI or model launch, heavy work, and any batch. Handoffs return to root.
