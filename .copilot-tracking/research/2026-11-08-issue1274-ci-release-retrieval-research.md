---
title: Issue 1274 hosted CI release retrieval research
ms.date: 2026-11-08
---

Task: `issue1274-ci-release-retrieval`. Research disposition: `executed`.
Branch `fix/ci-release-retrieval-1274`, base Main `0f05e9aae70768def8d1d9c300215f9ee2f11638`
(re-fetched 2026-11-08, `origin/main` unchanged). Logs are treated as data.

## Evidence

| Id | Finding | Evidence |
| --- | --- | --- |
| E1 | `src-namespace` / `Native workflow actionlint` fails with `curl: (22) ... error: 504`, exit 22, on `feat/formal-complaints-adapter-86` head `fb7231c788aa49d5dbcd7e30bd81c4806fea3cbf` (#1243). | `gh run view 42469282088 --log-failed`, job `128696067639`, 2026-11-08T10:01:37Z. Tool/unit/ruff steps passed first. |
| E2 | Same step, same 504, on #1271 attempt 2 (Source, namespace job). | Coordinator log `1271-source-attempt2.log` line 18-19, 2026-11-08T09:11:12Z. |
| E3 | Scorer `Install AWF binary` (`install_awf_binary.sh v0.28.23 --rootless`) gets six consecutive 504 responses at 10 s spacing, so the upstream installer already retries and still exhausts. | `1271-scorer-attempt2.log`, 09:01:48Z-09:02:49Z. |
| E4 | #1273 / c162 namespace and scorer failures are preserved. Only the 1243 and 1271 logs were consumed completed-job; no claim is made that c162 shares the cause. | Coordinator `pr530-c162-body.md`, `review-530-c162/`. |
| E5 | Live reproduction today: `HEAD https://github.com/rhysd/actionlint/releases/download/v1.7.7/actionlint_1.7.7_linux_amd64.tar.gz` returns HTTP 504 (content-length 92). | Local `curl -I -L`, 2026-11-08. |
| E6 | Official API asset endpoints work: `https://api.github.com/repos/rhysd/actionlint/releases/assets/221573254` (archive, 2080472 bytes) and `.../221573261` (checksums, 1119 bytes) with `Accept: application/octet-stream`. SHA-256 archive `023070a287cd8cccd71515fedc843f1985bf96c436b7effaecce67290e7e0757`, checksums `ac22e6577b8d133c7cd779682e65712ef722e719a297633699a4da05e9f351e0`. The checksums file lists the archive hash for `actionlint_1.7.7_linux_amd64.tar.gz`. Archive contains the `actionlint` binary. Nothing executed. | `gh api repos/rhysd/actionlint/releases/tags/v1.7.7`; independent download and `sha256sum`, matches coordinator probes. Release `digest` field is null. |

## Affected paths

* `.github/workflows/src-ci.yml` step `Native workflow actionlint` (job `namespace`, check name `src-namespace`): single-shot `curl -fsSL` with no retry, timeout or fallback; checksum comes from the same remote, so it only guards corruption, not identity. This is the owned fix target.
* `tools/rpi-checks.py` only reads an installed `actionlint` (`-version`); it does not download. Unchanged.
* `.github/workflows/rubric-score.lock.yml`: compiler-generated (gh-aw v0.89.21, DO NOT EDIT). AWF install is `github/gh-aw-actions/setup@924af5f...` upstream script. No repository source hook (`rubric-score.md` has no AWF install option checked) was identified; a hand edit is unsupported. Recorded as a partial blocker; no workaround.
* Synthetic unit failure prints in `tools/test_rpi_checks.py` and infra tests that contain `error`/`504`-like text are test output, not failures.
* `infra/tests/test_pipeline.py` tests the workflow structure and names; `WORKFLOW_HASHES` in `tools/rpi-checks.py` must be updated for `src-ci.yml`.
* `tools/ci-affected.py` `NAMESPACE_ONLY` and the `src-ci.yml` `paths` filter decide which jobs run on tool changes; new tool files need entries or the namespace job would be skipped or force everything.

## Options

1. Bash retry loop in the workflow. Rejected: not unit testable for truncation, wrong checksum or exhaustion.
2. New stdlib Python installer `tools/install-actionlint.py` with bounded retry per official source (browser URL, then official API asset), pinned archive and checksums digests, atomic fail-closed install, plus unit tests, called from the workflow. Selected.
3. Mirror or third-party installer action. Rejected by the issue (no mirrors, unverified fallback).

## Constraints and decisions

* Exact version `1.7.7`, asset names and ids, and both SHA-256 values pinned in code; the checksums file must also agree.
* Retry 5xx, 429, network, timeout and short or truncated body; 4xx other than 429 moves to the next official source immediately. Bounded attempts and a deadline; exhaustion exits non-zero and leaves no binary.
* Token optional (`GITHUB_TOKEN` already available, `contents: read`), sent only to `api.github.com` and dropped on redirect, never printed.
* Existing job name, check names and `permissions: contents: read` unchanged.
* Resume route for dependent PRs (#1243, #1271, #1273): workflow source is read from the PR merge/head commit, so old runs never consume this fix. After merge, each PR needs its own branch to contain the new `src-ci.yml` (normal base update when the owner chooses it) and a fresh run on that head. A rerun of an old run reuses the old workflow. No blind rerun or push churn is made here.
* AWF (E3) remains blocked on upstream or recompile; no repository-side workaround.

Planning Readiness: `Ready`.
