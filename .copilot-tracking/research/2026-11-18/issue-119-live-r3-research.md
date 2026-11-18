---
title: Issue 119 live evidence screenshot name review (r3 research)
ms.date: 2026-11-18
---

## Scope

Brief (2026-11-18): check whether the first-run issue 119 live evidence on `main`
(c94c4f0fa, PR 2051) holds screenshots showing resident or officer names, and
remove them in a docs-only commit. No `docs/reference/issue-119-live` folder exists;
the research notes are `docs/reference/research/issue-119-live*-map-evidence-2026-11-18.md`
and the screenshots live in `.copilot-tracking/evidence/2026-11-18/issue-119-live*/`.

## Method

Each PNG was opened and read visually; SHA-256 recorded to detect duplicates.

## Findings

| File | Names visible | Detail |
| --- | --- | --- |
| issue-119-live/map-list-open-1366.png | Yes | Resident names in the map list links (demo resident names) |
| issue-119-live/keyboard-focus-list-1366.png | Yes | Same list |
| issue-119-live/tiles-blocked-list-works-1366.png | Yes | Same list |
| issue-119-live/keyboard-opened-case-1366.png | Yes | Case header name, a named access contact and two officer names in the Owner block |
| issue-119-live/landing-no-map.png | Yes | Briefing lists named residents |
| issue-119-live/map-desktop-1366.png | No | Overview tiles and map only; SHA-256 identical to r2 `landing.png` and `map-desktop-1366.png` |

All data is the synthetic demo dataset, but the brief asks for removal of named screenshots.

## Residual finding (not changed)

`probe2.json` and `probe3.json` under issue-119-live (and `probe2.json` under issue-119-live-r2) held the same names as link text. Resolved at independent review: redacted to `[name removed]`.
