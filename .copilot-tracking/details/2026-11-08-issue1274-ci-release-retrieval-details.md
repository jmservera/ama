---
title: Issue 1274 hosted CI release retrieval details
ms.date: 2026-11-08
---

## Installer contract (`tools/install-actionlint.py`)

* Constants: `VERSION=1.7.7`; archive asset id 221573254, name `actionlint_1.7.7_linux_amd64.tar.gz`, size 2080472, SHA-256 `023070a2...0757`; checksums asset id 221573261, name `actionlint_1.7.7_checksums.txt`, SHA-256 `ac22e657...51e0`.
* Sources per asset in order: `https://github.com/rhysd/actionlint/releases/download/v1.7.7/<name>`, then `https://api.github.com/repos/rhysd/actionlint/releases/assets/<id>` with `Accept: application/octet-stream`.
* Per source: 3 attempts, 30 s timeout, delays 2 s then 5 s, body cap 8 MiB. Retry on HTTP 5xx/429, URL errors, timeouts, short body or digest mismatch. Other 4xx skips to next source. Exhaustion raises, exit 1, nothing installed.
* Digest is checked against the pinned value before use. The checksums file must contain the pinned archive digest for the archive name. Archive must contain a regular `actionlint` member, which alone is extracted to a temp file in the destination directory then atomically renamed, mode 0755.
* `GITHUB_TOKEN` is sent only to `api.github.com` and is dropped on redirects; never printed.
* CLI: `install-actionlint.py <dest-dir>`; prints the installed path only.

## Workflow

Step `Native workflow actionlint` runs the installer with `GITHUB_TOKEN`, then runs `"$RUNNER_TEMP/actionlint" -version` equality and the existing lint command. Job name, permissions and checks unchanged.

## Validation commands

```text
python3 -m unittest discover -s tools -p test_install_actionlint.py -v
python3 -m unittest discover -s tools -p test_ci_affected.py -v
python3 -m unittest discover -s tools -p test_rpi_checks.py
python3 -m unittest discover -s infra/tests -p test_pipeline.py
ruff check/format --isolated; mypy --strict
actionlint -config-file infra/tests/actionlint.yaml <five native workflows>
```
