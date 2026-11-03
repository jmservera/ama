<!-- markdownlint-disable-file -->
# Issue 107 R1 model bounds: research

Disposition: executed. Planning Readiness: Ready.

## Merged delivery (not redone)

* PR 287 (release admission for the five assistants), PR 293, R1 dispatch rebuild (PR 301), and core `assistant_release.py`, `rai_release.py`, `assistants.py`, `continuity.py` carry the 5 base criteria and 5 of the 9 RAI release criteria (see `src/agents/README.md`, "Release admission").
* #432 ledger (`ai_consumption.py`) already carries `max_calls` and `max_depth` on a financial authority, but no per-assistant statement exists for the five assistants.

## Unmet criteria (evidence-based)

* RAI release: persisted release record with approver is built, but approvers unset (`ZF_ASSIST_RELEASE_APPROVERS`), OQ-017 authority open; serving attestation, Azure SQL race tests, delivered-build acceptance unmet.
* Tokenomics 1: no stated per-assistant maximum calls and depth, no test. Smallest coherent slice, code-only, no security/SQL/infra/deployment change.
* Tokenomics 2 (usage attribution) and 3 (proactive forecast per period): unmet, later slices.

## Facts

* Worker `AgentWorker.handle` makes exactly one provider call per task attempt, `CallContext.depth` defaults to 1, no tools in `SYSTEM`.
* Attempts per request are `Limits.attempts`, bounded to 1..3, enforced in `Assistants.claim` (`attempts >= l.attempts`).
* Adding fields to `REGISTRY` would change `registry_hash` and dedupe identity, so the bound is a separate constant.

## Slices

1. This slice: model-call and depth bound statement and tests (Tokenomics 1).
2. Later: proactive predicate forecast of calls per period (Tokenomics 3).
3. Later: per-assistant and per-accepted-proposal usage attribution (Tokenomics 2).
