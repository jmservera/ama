<!-- markdownlint-disable-file -->
# Changes: #74 home case regression slice (issue-74-home-case-regression-2300)

Date 2026-11-12. Base eac1206c6ca08bd551e3d0d2384bb87a1f05c24f. Test-only; no product source, workflow, dependency or deployment edit. Plan: [plan](../../plans/2026-11-12/issue-74-home-case-regression-2300-plan.md). Critique (independent, before implementation): [critique](../../plans/2026-11-12/issue-74-home-case-regression-2300-critique.md).

## Files changed

* `src/api/tests/test_home_case_api.py`: two HTTP tests appended after the last test (G3, G4). Non-finance staff (`sam@example.test`) get the restriction flags and no "6000.00", "12000.00", "SYN-ALLOCATION" or "SYN-ESTIMATE" anywhere in the body for ZF-2 and ZF-3. Finance staff (`pam@example.test`) get allocation 6000.00 and building cost 12000.00 with the exact record shape. No `funding_confirmed` assertion.
* `src/api/checks/home_case_browser_check.py`: `home_case_data()` seeds ZF-2 with its own document "Synthetic own-home survey" and quality "Ventilation extract". New checks: ZF-2 shows them in the home region only; the exact system item `SYS-1: Shared ventilation Source: SYN-SURVEY` is in the building region only (G1); a ZF-3 page, opened after the existing reflow and axe checks, shows its own sibling document and quality in the home region, none of ZF-2's own tokens, the same system rule, GBP 6000.00 at home and GBP 12000.00 only in the building region (G2). Existing checks, the ZF-2 reflow and axe scan, and the write guard are unchanged.

## Validation (focused tier; synthetic data; pip venv at the external evidence root)

External evidence directory: `/home/azureuser/.copilot/session-state/38e61c82-3c44-4b97-af59-9eed5c151ac7/files/rpi-74-2300-evidence/`.

* API tests `test_home_case_api.py`: 5 OK (`api-final.out`). Core `test_home_case.py` (impacted regression): 7 OK (`core-final.out`). ruff check, ruff format and mypy on both files clean.
* Browser check with pinned axe 4.10.3 (sha256 880970c0...8bb verified by the check itself) under `/tmp/ama-rpi-heavy.lock`: 24 PASS, COMPLETE (`browser-final.out`).
* Mutation controls (scratch only; the repository tree was never mutated). Browser, from an external scratch copy of `src/`: M0 unmutated baseline passes. M1 own document dropped, M2 own quality dropped and M6 seed without own document each fail "ZF-2 shows its own document and quality in the home panel only". M3 own document leaks onto ZF-3 and M4 own quality leaks onto ZF-3 each fail "ZF-3 view carries none of ZF-2's own document or quality". M5 system moved into the home region fails the ZF-2 system check; M8 fails the ZF-3 system check; M7 ZF-3 quality dropped fails the ZF-3 own-evidence check. API, on venv copies of core (restored and hash-verified): A1 allocation leak fails the allocation flag assertion (line 128), A2 building cost leak errors with KeyError on the building flag (line 130; detected as a test error, not an assertion failure), A3 allocation hidden from finance fails line 141, A4 building costs hidden from finance fails line 146.

## Adverse and corrected outputs preserved

* `browser-first-run-adverse.out`: the first browser run failed my own assertion because the rendered system item has no period before "Source:" when there is no status. The expected string was corrected, not the product.
* `mutation-M8-first-run-adverse-invalid-js.out`: the first M8 mutation produced invalid JavaScript, so the page never loaded; it proved nothing and was rerun with a valid mutation.
* `adverse-cumulative-state-mutation-A1..A4*.out`: the first API mutation run did not restore the other core file between mutations, so A2 and A4 ran on top of A1 and A3. Discarded as controls and rerun from clean baselines.
* Admission precision: the #82 branch diff lists `test_home_case_api.py` (path overlap, hunk-disjoint, contrary to a plain "disjoint" statement). Tests were appended at the end of the class to avoid a textual conflict.

## Limits

Not run: complete local gate, `--changed`, hosted CI (no push), SQL Server, manual assistive technology. Chromium only. Isolation claims cover the seeded sentinel records only; shared document names (SYN-EPC, SYN-Design, SYN-Consent) are identical across the homes. Criterion 2 is not proven or ticked; the outcome tuple and G5 are untouched; no owner approval is implied. A PR would use `Refs #74`.
