---
title: Issue 1274 hosted CI release retrieval plan
ms.date: 2026-11-08
---

Research: [research](../research/2026-11-08-issue1274-ci-release-retrieval-research.md).
Details: [details](../details/2026-11-08-issue1274-ci-release-retrieval-details.md).
Critique: [critique](../plans/2026-11-08-issue1274-ci-release-retrieval-critique.md).

## Phases

* [x] P1 Add `tools/install-actionlint.py`: pinned exact version, bounded retrieval from official browser URL then official API asset, size and digest validation, safe single-member extraction, fail closed.
* [x] P2 Add `tools/test_install_actionlint.py`: 504 then recovery, source fallback, truncated, invalid archive, wrong checksum, checksums mismatch, exhaustion, no-binary-on-failure, token not forwarded across hosts.
* [x] P3 Update `src-ci.yml` (step body, `paths`, tool test/ruff/format/mypy lines), `tools/ci-affected.py` `NAMESPACE_ONLY` plus its test, `WORKFLOW_HASHES`.
* [x] P4 Validate: new and existing tool tests, `tools/test_rpi_checks.py`, `tools/test_ci_affected.py`, infra pipeline tests, ruff, format, mypy strict, real actionlint run on the real verified archive with the repository config.
* [x] P5 Docs/log entry, changes record, review, commit.

## Non-goals

AWF bootstrap in the compiler-generated scorer lock (partial blocker), mirrors, protection changes, push or PR.
