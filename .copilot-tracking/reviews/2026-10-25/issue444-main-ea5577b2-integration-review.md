# Issue 444 round-3 PR boundary review

Date: 2026-10-25. Executed once by an independent code-review agent over `git diff origin/main...HEAD` on the rebased head (before any correction). Earlier reviews are preserved unchanged.

## Outcome

Conformant with follow-ups. Review execution: yes. No Critical or High findings. The reviewer ran the 31 core and 14 api resident tests (pass).

## Findings and dispositions

| # | Severity | Finding | Disposition |
| --- | --- | --- | --- |
| 1 | Medium | Stage text "Survey booked" and "Install booked" asserted a booking regardless of appointment state; "Check the confirmed arrangements below" could point at a section that is not shown. Weakens offers vs confirmed and unknown stays unknown. | Correction cycle 1 (see changes artifact): neutral wording, regression test. |
| 2 | Low | Footer link opens raw JSON (/resident/about). | Routed follow-up; no web change in this run. |
| 3 | Low | Web-interface-guidelines items: three dots instead of ellipsis, noscript shown under a permanent loading status, no theme-color/color-scheme, no translate=no, main:focus outline none, no touch-action, no text-wrap balance, possible empty home card, possible double announcement of errors, focus drops after Try again. | Routed follow-up; recorded, none fixed here. |
| 4 | Known Low | Grants re-read per request but dataset, case and representative-authority data load once; dataset authority edits need a restart. | Explicit retained limitation. |

## Verified by the reviewer

Default-deny grants, identity, representative authority, allowlist projection, unavailable actions, XSS, CSP, host check, startup guards, resident source identical to backup/444-pre-round3-ab07351a, one additive pyproject line.

## Not verified by the reviewer

Browser check and rendered visuals, mypy/ruff, fixture canary contents beyond tests, CI and gates, the tracking artifact content, load, live HTTP, contrast measurement, domain functions beyond call sites. No human screen-reader audit; Fluent 2 partial; no conformance claim.
