# Critique (rubber-duck, independent, 2026-11-13)

Verdict: Proceed with changes. Executed once; no tests were run by the critic.

1. Blocking: harness needs assertions (offsets, rows, boundary call counts, pager absence, status text) that fail on mismatch. Applied.
2. Blocking: editable installs and test caches may write under src or use network. Applied: use `--no-build-isolation`, `PYTHONDONTWRITEBYTECODE=1`, check `git status --short` after, remove generated egg-info.
3. Non-blocking: empty operator input ambiguity. Applied: run both the data-operator `render({id})` empty and the exception-register empty tests, asserting existing text.
4. Non-blocking: mocked `h()` is not a browser DOM; no AT/WCAG claims; missing disabled/aria-disabled is an observation. Applied.
