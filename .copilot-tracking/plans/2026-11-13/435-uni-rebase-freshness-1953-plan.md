---
title: 435 unified rebase plan
ms.date: 2026-11-13
---

## Plan

1. Stash nothing; move tracking files aside is unnecessary (untracked, outside commits). Rebase topic onto `dab0b0893`.
2. Cherry-pick `e1834dfc6`, `142824c30`, `6124aee61`; resolve conflicts keeping both sides.
3. Regenerate inventory with `cutover_audit.py --write`; run `--check` mode.
4. Re-run the #441 C9 verifier; require `freshness: true` and `overall_ok: true`.
5. Run `test_cutover_audit`, `validation.json` hash check, relative link check, secret scrub.
6. Independent `code-review-readiness`, commit (no push). Tier Focused.

Details: remove own venv path only; use pip. Critique by `rubber-duck` before implementation.

## Critique (rubber-duck, one pass)

* Check mode is `cutover_audit.py` with no flag, not `--check`; applied.
* Verifier freshness requires `docs`/`src` at HEAD to equal `origin/main` and a clean tree outside tracking, which an unmerged docs branch cannot satisfy before merge. Run it as specified and report the true result; do not alter the verifier or the report.
