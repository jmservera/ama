# Details: orchestrator verification

Write surface: `.copilot-tracking/` only. No `src/` or `docs/` edits.

## Commands

```bash
python3 -m venv --system-site-packages /tmp/venv-orch-1143
/tmp/venv-orch-1143/bin/pip install --upgrade setuptools wheel
for p in core agents importer orchestrator; do /tmp/venv-orch-1143/bin/pip install --no-deps --no-build-isolation -e src/$p; done
/tmp/venv-orch-1143/bin/python -c "import zava_forward.core as c, zava_forward.orchestrator as o; print(c.__path__[0], o.__path__[0])"
cd src/orchestrator
env -u ZF_DATA -u ZF_TEST_MSSQL PYTHONPATH=../core/tests /tmp/venv-orch-1143/bin/python -m unittest discover -s tests -v > /tmp/orch-1143.log 2>&1; echo $? > /tmp/orch-1143.rc
```

## Critique amendments

* Use `set -e`, `PYTHONDONTWRITEBYTECODE=1`, and `env -i PATH=... HOME=/tmp/orch-home PYTHONPATH=../core/tests PYTHONDONTWRITEBYTECODE=1` for the test run.
* Assert every `__path__` entry for core, agents, importer and orchestrator is under the worktree `src/`.
* After the run, delete untracked/ignored build artifacts under `src/` (egg-info, `__pycache__`) and verify none remain.
* Network denial cannot be enforced unprivileged; record as a limitation.

## Validation

* Exit code from the file, not a pipeline.
* Per-module counts parsed from the verbose log; skips listed verbatim.
* Log sha256 recorded; log copied outside the worktree or summarized only.
* Namespace package: `__path__` may list several entries; accept if all resolve inside worktree `src/`.
* No network: tests are expected offline; any attempt is reported, not worked around.
* Cleanup: remove `/tmp/venv-orch-1143` and scratch logs; check `git diff --check` and `git status --short` before commit.
