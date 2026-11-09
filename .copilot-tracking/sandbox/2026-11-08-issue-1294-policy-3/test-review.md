# Test review (run 3): independent grader return (fresh general-purpose subagent, model not observable, proxy)

Verdict: Revise. Simulation, proxy profile, model unresolved; hosted CI, a real runner and Chromium not exercised.

Scenario grades: S01 Pass, S02 Revise (F3), S03 Pass, S04 Pass, S05 Revise (F2), S06 Pass, S07 Pass, S08 Pass, S09 Pass, S10 Revise (F1), S11 Pass, S12 Pass.

Findings:
* F1 (correction, Low): ZF_BROWSER_SCRATCH sentence reads as self-contradictory (evidence src/README.md direct-check list; design_system_browser_check.py:228-240: unset falls back to <checkout>/.venv, set relative or in-checkout value raises ValueError). Fix: state unset and set cases separately.
* F2 (correction, Medium): mixed docs-plus-chat row "Never claim" cell "A full receipt as required" is ambiguous. Fix: "That a full receipt is required, or that hosted CI covers the harness".
* F3 (correction, Low): "selector and four other browser checks" not precisely supported by src-ci.yml:102-119 (employee_acceptance_check plus design_system, regulatory_ux, case_journey browser checks, plus the selector). Fix: name them.
* F4 (adjustment, Low): "HVE gates" undefined in the documentation row. Fix: name the hve-builder static, behavior and host gates.
Not defects: S09 coverage labels verified against the workflow; 58-byte limit correctly runner-specific (rpi-checks.py:94, 250-252, 1717); coordinator wording consistent.

Coverage misses: designer did not read tool/workflow files; no scenario targeted the coordinator mixed-tier sentence directly; a chat-change-plus-unresolved-workflow-edit mixed case and --verify-receipt currency were only touched in passing.
Limitations: proxy; stronger model may repair ambiguity; Chromium TMPDIR inheritance unmeasured (already flagged in the guide).
