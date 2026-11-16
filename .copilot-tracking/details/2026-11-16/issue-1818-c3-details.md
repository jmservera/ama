# Issue 1818 c3 details

Phase 1: edit line 145 of `src/api/checks/design_system_browser_check.py`: `get_by_role("button", name=re.compile(...))` with `re.escape` on the label; add `import re`.
Phase 2: validation commands from the task brief plus `python -m checks.design_system_browser_check`.
