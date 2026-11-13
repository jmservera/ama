---
title: "#232 keyboard/text browser observation, selectors 232 and 232s (2026-11-13)"
ms.date: 2026-11-13
---

Base: origin/main 347962dace94171724cc8db4044c8d783335fecf (see head.txt). Source tree hash
(core, agents, api src) in tree-hash.txt. No source, test, fixture or policy change.

## Research

* Read the `src/api/README.md` role screens guide and `checks/design_system_browser_check.py` `main`: a
  TemporaryDirectory under ZF_BROWSER_SCRATCH, synthetic data, a loopback 127.0.0.1 server, an environment
  stripped of credentials, ZF_STORE=json.
* Origins (origins.txt): `zava_forward.api` resolves to this worktree; the core namespace path lists this
  worktree first and a foreign worktree's editable install second (read-only reuse of
  `~/.cache/ama-venv-133-hooks-1110`, Python 3.12.3, playwright 1.64.0; not modified, nothing installed).
* No pinned axe 4.10.3 file was found (a filesystem search was stopped), so ZF_AXE_JS was unset.
* Guidelines fetched fresh: HTTP 200, sha256 d246b026..., see guidelines.md.

## Plan (prospective, as executed)

Run `python -m checks.role_screens_browser_check 232` then `232s` from `src/api` under a non-blocking
`flock -n /tmp/ama-rpi-heavy.lock` (no holder seen), `systemd-run --user --scope -p MemoryMax=2G
-p MemorySwapMax=0`, `timeout 150`. No retry.

## Critique

NOTRUN as an independent pre-execution critique within the ten-minute bound. This is a process deviation;
the independent post-hoc review below is the only independent assessment.

## Implementation (validation only)

Both commands exited 0 (run-232.exit, run-232s.exit); stderr empty; no FAIL lines. Chromium 156.0.8078.4.
Observed: text-stated choice, issue and commitment meaning; no write controls; Tab reaches the table regions
(232: three, 232s: one) at 1280 px; CSV download attachment (232). Axe: SKIP for both (no result).
Memory: free before 4.2 GiB available, no swap; the host was shared with other processes.

## Review (independent, rubber-duck agent, read actual outputs)

Verdict Partial for the narrow claim. Findings, all frozen and not corrected:

* 232s text meaning asserts the heading and panel title, not the issue state's explanation.
* Tab reach was observed at 1280 px only, by label match.
* The MemoryMax=2G effect was not captured (no cgroup property recorded).
* Foreign namespace-path fallback; other module origins not enumerated.
* Axe SKIP means no axe/WCAG result.

## Limits and remaining

Not assistive-technology, named-human, production, live or whole-issue acceptance. The literal #232 AC
(WCAG, textual meaning, keyboard) stays unchecked. Prior 0740 and 134 adverse records are unchanged.
