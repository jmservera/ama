# Plan: 136-bicep-verify-1045

* [ ] P1 Copy 7 ac6527569 tracking files byte-identically; verify sha256.
* [ ] P2 Create /tmp/venv-136-1045, pip install -e src/core; verify zava_forward.core __file__ under this worktree.
* [ ] P3 Run python -m unittest discover -s infra/tests -v; capture producer exit code, counts, skips.
* [ ] P4 Offline bicep build (stdout to /dev/null) for 5 files; capture exit codes and warnings.
* [ ] P5 Record changes, remove venv, review, commit.
Write surface: .copilot-tracking only.

Amendments from critique: see critique file dispositions (offline pip flags, unset ZF_API_IMAGE, PYTHONDONTWRITEBYTECODE=1, blob-hash verification, post-run git status check).
