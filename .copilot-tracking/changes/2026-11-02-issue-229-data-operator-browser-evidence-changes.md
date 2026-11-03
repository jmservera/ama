# Changes: issue #229 browser evidence slice

* `src/api/checks/data_operator_browser_check.py`: new browser check for the data steward and operator view (new file).
* `src/api/README.md`: one paragraph describing the check.

Validation (original): check passes with pinned axe 4.10.3 (zero violations, nothing incomplete), Tab reach of four table regions, 320px reflow, no POST requests. No production code changed.

## Correction note 2026-11-02 (after independent review FAIL)

* The original text claimed the gate passed and listed no divergences. That was wrong: `python3 tools/rpi-checks.py --changed --base origin/main --lock-timeout 600` has produced no receipt. Attempts: blocked by the original run's lock timeouts (four times); in the correction, once by "Candidate has ignored inputs" (local egg-info and bytecode from my own pip install, removed), once interrupted by my own 590 s wrapper timeout, and once more by "Global heavy-resource lock timeout" (`--out /tmp/gate779fix2`, because `/tmp/gate779fix` was consumed by the interrupted run). The gate is therefore NOT passed and must be rerun before publication.
* Browser check corrected: any request method other than GET, HEAD or OPTIONS after sign-in is a write (sign-in excluded); a skipped axe scan prints `RESULT PARTIAL` instead of passing; vacuous and OR-based assertions replaced by separate real assertions.
* Axe claim, qualified: axe-core 4.10.3 (SHA-256 pinned), run on `main` only, at 1280px, for the Retrofit Programme Manager role, on the Data steward and operator evidence view for synthetic home ZF-1 only, tags wcag2a, wcag2aa, wcag21a, wcag21aa, wcag22aa: no violations, no incomplete items reported in the verified run. It is not run when `ZF_AXE_JS` is unset. Automated checks cover only part of WCAG.
* Re-verified locally after the fix: check runs PARTIAL without axe and PASS with axe.
* Divergences: the gate result above differs from the original claim.
