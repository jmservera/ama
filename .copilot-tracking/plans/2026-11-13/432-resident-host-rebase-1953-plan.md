# Plan: 432 resident host rebase

1. Rebase: `git rebase --onto dab0b0893 edf4ccf14`; abort on conflict and report.
2. Create /tmp/venv-432hr-1953, pip install src/core, src/agents, src/api (+dev extras, playwright for mypy).
3. Run test_ai_call_site_inventory, test_ai_consumption* (core, api), test_resident_* non-browser, ruff, mypy.
4. code-review the rebased diff; commit if anything changes; remove only own venv; confirm clean status.
Critique (rubber-duck): verified HEAD/ancestry/single commit; venv path private (only I use it); targeted tests as brief.
