# Changes: issue #227 browser evidence slice

* `src/api/checks/safety_screens_browser_check.py`: new browser check for both safety screens (new file).
* `src/api/README.md`: one paragraph describing the check.

Validation: the check passed for both roles with pinned axe 4.10.3 on the original run. Axe scans `main` only at 1280px, so zero violations is partial automated evidence, not conformance. Axe is reported as SKIPPED (with a PARTIAL summary) when `ZF_AXE_JS` is unset. No production code changed.

Correction after independent review (2026-11-02): rebased onto origin/main; the write check now records any method not in GET, HEAD or OPTIONS; skipped axe is visible. Gate: focused tier `python3 tools/rpi-checks.py --changed --base origin/main --lock-timeout 600 --out /tmp/gate227fix` returned VERIFIED partial local gate for head 8e2180ca64301e64f0e4faba79bbf5308f16f950 on base 627aed6fb52b37d11191699ad9c256e8ca761555 (21 browser states, axe executed, no skips; receipt /tmp/gate227fix/receipt.json, external and not committed). Earlier attempts were BLOCKED by a stale ignored `__pycache__` (removed), main advancing during the lock wait (rebased), and repeated global heavy-lock timeouts from concurrent runs. Independent exact-head review, hosted CI and human/AT acceptance remain pending.
