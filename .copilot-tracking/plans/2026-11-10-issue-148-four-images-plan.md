<!-- markdownlint-disable-file -->
# Plan: issue 148 four-workload image wiring

Readback 2026-11-10T01:30Z. Research: `.copilot-tracking/research/2026-11-10-issue-148-four-images-research.md`. Details: `.copilot-tracking/details/2026-11-10-issue-148-four-images-details.md`. Prospective: written and committed before any source edit. Targeted tier; owned source files only `src/orchestrator/src/zava_forward/orchestrator/rebuild_azure.py` and `src/orchestrator/tests/test_rebuild_azure.py`. Default five-total review correction budget applies to the lifecycle; this plan assumes zero corrections used.

## Steps

* [ ] 1. Commit these records (research, plan, details, critique, state) before source edits.
* [ ] 2. Extend the fake `az` and add regressions; run them against UNCHANGED source and record the expected failures.
* [ ] 3. Implement the four-workload table, build loop, verification, resume guard, explicit mapping, reserved parameters and static dry-run listing.
* [ ] 4. Run impacted orchestrator tests, ruff check/format, mypy; record exact counts.
* [ ] 5. Record changes and review; commit source and records; freeze candidate locally; write handoff.

## Behaviour

* Table: api -> `zava-forward-mvp` -> `apiImage`; agents -> `zava-forward-agents` -> `agentImage`; importer -> `zava-forward-importer` -> `importImage`; orchestrator -> `zava-forward-orchestrator` -> explicit `--orchestrator-image` (deploy.py rejects it as a parameter).
* `images` stage builds all four in table order with `src/<project>/Dockerfile`, context `<repo-root>/src`, the pool when set, tag `<repo>:<image-tag>`. First failing build stops with a `RebuildError` naming the project and chained to the original `ScriptExit`; later builds and the deploy never run.
* `images` verify and the `applications` deploy share one check: every repository must list the exact tag; a missing repository (az error) or tag is reported by project. The deploy checks before any `deploy.py` call, so a resume at `applications` with only the API tag stops with the `--from-stage images` instruction.
* Applications deploy passes the three parameters and `--orchestrator-image`, all `<login-server>/<repo>:<tag>`; never `latest`, placeholder or a discovery guess. `agentImage`, `importImage`, `orchestratorImage` become reserved override names.
* Dry run: `plan()` adds a static `images` listing; still no I/O.
* Unchanged: first gated-stage stop, timeouts, teardown, dependency deploy (`deployApplications=false`).

## Out of scope

Digest pinning, real builds/Azure, doc edits, deploy.py/Bicep/pipeline, #144 workers.
