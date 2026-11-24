# Critique: issue 1204 live (2026-11-24), executed once

Verdict: proceed with amendments, applied directly.

* Risk: a flag that changes defaults would break legacy windows. Amendment: opt-in `--require-extended`; default behaviour unchanged.
* Risk: sqlite loader only sets keys for existing columns, so a missing column shows as an absent key. Amendment: one check on key presence in `check_ticks(require_extended=True)` covers both input types.
* No `src/` change, so tier FOCUSED; no Azure use.
