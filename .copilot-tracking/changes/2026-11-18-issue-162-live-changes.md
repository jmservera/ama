---
title: Changes for #162 live break-glass proof
ms.date: 2026-11-18
---

## Files

* Added `docs/reference/research/chat-breakglass-live-proof-2026-11-18.md` with `chat-breakglass-live-proof-2026-11-18/` (probe script, login helper, desktop screenshot).
* Updated `docs/reference/README.md` index and appended `docs/reference/log.md`.
* No `src/` change. Tier FOCUSED. `rpi-checks.py --all` not run.

## Per-criterion table

| Criterion | Status | Evidence |
| --- | --- | --- |
| 1 to 5 | Already ticked, not re-opened | Issue body |
| 6 audited (refusals) | Proven live | Each refused attempt adds one audit entry, chain intact (1517 to 1519) |
| 6 audited with purpose (grants) | Unproven live; proven by unit tests | Needs a config change on the app; 33 tests OK |
| 6 policy decided | Decided for the demo only | 2026-11-03 owner disclaimer; Entra role, notification, retention undecided |
| 6 overall | Not fully proven live; left unticked | See research note |

## Validation

* `python3 -m unittest tests.test_chat_isolation` from `src/api`: 33 tests OK.
* Markdown link and diff review. mypy and ruff not applicable (no Python source change; the probe script is evidence, not package code).
* Hosted CI: not run (nothing pushed).

## Divergences

* Over-broad cleanup: all ~15 empty "New chat" threads of the staff test user were deleted, not only the probe's thread. Synthetic data, own user only; disclosed in the research note.
* The documentation was written before the `implement-start` witness call; the call records the changes file as it stood.
