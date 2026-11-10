<!-- markdownlint-disable-file -->
# Review: issue 148 four-workload image wiring

Readback 2026-11-10T01:47Z. Executed once by the implementing agent (no nested agents). Boundary: local diff of the two owned files plus original records at the frozen head. Outcome: `conformant locally; independent exact-head review still required`.

## Checks

* Scope: only the two owned source files changed; no deploy.py, Bicep, pipeline, worker, docs or app files.
* Contracts: parameter names `apiImage`, `agentImage`, `importImage` and option `--orchestrator-image` match `infra/main.bicep`, `deploy.py` and `pipeline.py`; repositories follow `zava-forward-<project>` with the legacy API repository kept.
* Fail-closed: build failure, missing/unreadable tag and API-only resume stop before the application deploy; verified by new tests that fail on the old source.
* Preserved: dry-run no I/O, first gated stop (exit 2), timeouts, teardown, dependency deploy, original `ScriptExit` text and cause.
* Secret guard: image references pass `assert_no_secret_argv`; no token on argv.

## Open items routed to later work (not corrected here)

* Digest pinning of the four images (stage text says "pinned to digests"; adapter verifies tags). Same-tag staleness on resume is therefore possible.
* `infra/README.md` and `src/orchestrator/README.md` describe the images stage generically; update when docs are owned.
* Disposable Azure rebuild (criterion 4), workload SQL/model probes: unchanged and unmet.
* Four sequential `acr build` calls extend wall time; each keeps the 3600 s timeout.
