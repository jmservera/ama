# Plan: issue 230 programme screen browser proof

1. Add scenario `230` to `src/api/checks/role_screens_browser_check.py` with a dedicated fixture wrapper that makes the shared fixture's return the active return for ZF-1.
2. Drive the programme queue as Retrofit Programme Manager and Retrofit Coordinator: queue columns, role-scoped withholding for the coordinator, keyboard focus order (select, Apply, Reset, Shift+Tab, Space), visible focus, non-mutating filter and reset (case record equal before and after, no non-GET requests), five-gate table with textual Blocked states, no role simulator, reflow, no JS errors.
3. Optional axe scan via `ZF_AXE_JS` with SHA-256 pin; skipped explicitly when absent.
4. Document in `src/api/README.md`.
5. Validate: scenarios 230, 232 and parent pass; `rpi-checks.py --changed`. (Correction 2026-11-02: the focused gate was blocked by a heavy-resource lock timeout and has not passed; see changes note.)

Critique (inline, once): keep to the check harness; no web changes unless axe or keyboard checks fail; do not claim WCAG or assistive-technology acceptance. Accepted. Result: no web fixes were needed.
