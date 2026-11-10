<!-- markdownlint-disable-file -->
# Details: closed-stdin refusal D1

* Source: first statement inside the existing `try` in `main`: `if sys.stdin is None: raise ValueError("standard input is closed; pipe one constructed JSON object on standard input.")`. The existing `except (ValueError, RecursionError)` writes the single `Learning report refused: ...` line and returns 1. The tty check and read follow unchanged.
* Test: one method in `ConstructedReportCommand`. It runs the real module with `subprocess.run` in a fresh empty temp cwd with the same `ZF_DATA` nonexistent-path environment as `command`, closing descriptor 0 in the child through `preexec_fn` so the child genuinely has no stdin. Asserts return code 1, empty stdout, stderr exactly one line starting `Learning report refused: `, no `Traceback`, and an empty temp directory. No mocking of `sys.stdin`.
* Checks (from `src/core`, venv `~/.venvs/issue129-learning-cli-1110`: Python 3.12.3, ruff 0.17.1, mypy 2.4.0 pinned in `pyproject.toml`): `python -m unittest discover -s tests -p test_learning_test_bundles.py -q`; `ruff check .`; `ruff format --check .`; `mypy`.
