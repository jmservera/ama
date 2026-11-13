# Changes: refill correction 2 (issue 1204)

Plan, research and prospective critique were persisted before any source edit (see [critique](../plans/critiques/2026-11-13-demo-permanent-refill-1204-0914-c2-critique.md)). Original records untouched.

* Agent file only: exit-2 handling inspects each reported session's log and recorded exit status, classifies finished versus failed start, refills and re-arms, never ends the delivery run; continuation eligibility (dependencies, finite permission, selected validation, run-owned source) with missing approval `human-blocked` and unknown as bounded investigation; the other "ready" bullet qualified the same way; launch command replaced by a bash launcher example (quoted heredoc, args name/stamp/brief-path, `PIPESTATUS[0]` right after `tee`, exit appended and returned, append-only per-session log), run as `bash /tmp/launch-...sh`; `{name}` used for session, log, witness `--session`, has-session, capture-pane and kill-session.

Checks (exit 0 unless stated): `bash -n` on the launcher extracted from the agent file; the extracted launcher run with a stub `copilot` (exit 7 returned as 7 and logged `exit=7`; success 0; two attempts appended; brief path with a space passed correctly); 6 helper unit tests; CI-profile ruff check and format. No real Copilot/model run.

Closure: two targeted independent code-review passes (runtime-default model). First found the role-session brief/name inconsistency (fixed); second found residual `rpi-{number}` tmux commands (fixed); the final edit was not re-reviewed beyond a grep of the three tmux sites.

Remaining gate limitation: HVE behavior-gate testing with the canonical test model is Deferred (owner unavailable); no intended-profile Pass is claimed. The original static traces are not a canonical behavior-gate Pass.
