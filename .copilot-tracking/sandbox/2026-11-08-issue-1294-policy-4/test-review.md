# Test review A1 (sandbox 4)

Grader: fresh general-purpose subagent (c3-grader-a1), read-only, confined to the issue contract; actual model not observable (proxy). Executed: independent of designer and executor.

Overall verdict: Pass. Confirmed contract defects: 0.

| Scenario | Grade | Basis |
| --- | --- | --- |
| S01 | Pass | src-ci.yml path filter excludes docs/ and .github/copilot-instructions.md; guide says no Source CI run is expected |
| S02 | Pass | commands and acceptance rules match code (employee_chat_browser_check, rpi-checks.py 1560-1574, employee_acceptance_check.py 510) |
| S03 | Pass | SQL full tier, commands, local-only selector |
| S04 | Pass | full; --changed partial; hosted src-namespace correct |
| S05 | Pass | focused+focused stays focused |
| S06 | Pass | any full component makes whole full |
| S07a | Pass | impact-based with recorded basis |
| S07b | Pass | image/package and unresolved impact full |
| S08 | Pass | shared/local-only/hosted-only labels match workflow and runner |
| S09 | Pass | 58-byte limit is the runner's only (107-45=62, minus 4 for /tmp; rpi-checks.py 243-256); ZF_BROWSER_SCRATCH behavior verified |
| S10a | Pass | unpublished means unobserved; all-steps-skipped matrix is not a pass (ci-affected.py selects nothing for src/*.md) |
| S10b | Pass | missing prerequisites block publication; no fallback |
| S11 | Pass | correction entry truthful about tested revision |

## (b) Nonblocking observations (not defects, no edit)
* COORD line 478 "mixed work takes the full tier if any part requires it" is consistent with the strictest-tier rule but silent on focused+focused (README and instructions state it).
* README line 188 gives no commands for unit/lint/types (generic commands at lines 53-55).
* README does not say where the axe file lives or where AXE_SHA256 is defined.
* No exact handoff wording for S01; S10a prompt internally inconsistent; S04 reading is inference; tooling planned checks not enumerated.

## Evidence quality and limits
Design independent (checklist only, no .copilot-tracking). Executor trace literal with line citations and observed/inferred labels. Containment reported by executor; lead re-checked git status (only expected files). Not re-verified by grader: executor containment. Result applies to HEAD bd63b22 plus the uncommitted C3 edits only. Proxy profile, simulation only; hosted CI unobserved; untested: timing, --resume, receipt schema, branch/PR workflow, retention wording, real browser run, mixed workflow+docs, coordinator tier-reassessment rule.
