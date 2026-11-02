# Changes: issue #227 browser evidence slice

* `src/api/checks/safety_screens_browser_check.py`: new browser check for both safety screens (new file).
* `src/api/README.md`: one paragraph describing the check.

Validation: the check passed for both roles with pinned axe 4.10.3 on the original run. Axe scans `main` only at 1280px, so zero violations is partial automated evidence, not conformance. Axe is reported as SKIPPED (with a PARTIAL summary) when `ZF_AXE_JS` is unset. No production code changed.

Correction after independent review (2026-11-02): rebased onto origin/main; the write check now records any method not in GET, HEAD or OPTIONS; skipped axe is visible. Gate: `python3 tools/rpi-checks.py --changed --base origin/main --lock-timeout 600` was rerun and returned BLOCKED ("--out is required and must be a new external directory"); the gate has not passed. Divergence: the owner-specified gate command omits `--out`, so it cannot complete as written.
