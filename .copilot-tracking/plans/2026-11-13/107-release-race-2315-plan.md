<!-- markdownlint-disable-file -->
# Plan: Issue #107 release record, serving attestation, race tests

* Research: [107-release-race-2315-research.md](../../research/2026-11-13/107-release-race-2315-research.md)
* Details: [107-release-race-2315-details.md](../../details/2026-11-13/107-release-race-2315-details.md)
* Validation tier: Focused (venv `/tmp/venv-107-2315`, pip only)

## Phases

* [x] P1: `rai_release` validators for scope, frozen evaluation summary, consumption config; `attest_serving`.
* [x] P2: `assistant_release.record` persists the new fields; fixtures and README updated.
* [x] P3: `assistants.complete` persists attestation and an explicit fallback; event emitted.
* [x] P4: Tests: core unit tests and SQL/race tests (in-flight revocation, restart, new-record re-enable, attestation persistence).
* [x] P5: Focused validation, review artifact, Conventional commit with trailer, no push.

## Critique (one pass, direct dispositions)

* Verdict: Approve with comments. Compatible findings applied directly: keep schema unchanged; make older records fail closed; keep response `model` described as returned-model attestation, never as independent control-plane proof; do not touch infra, monitoring_coverage or ranking_publish; do not tick #107.
