# Issue 444 boundary threat model documentation: plan

Date: 2026-10-25. Prospective; written after the research and before any content change. Details: details/2026-10-25/issue444-boundary-threat-model-details.md.

* [ ] Phase 1: critique this plan once (independent), apply compatible findings, commit research, plan, details, critique and state before the documentation edit.
* [ ] Phase 2: add the threat-model subsection to src/api/README.md and a link in src/core/README.md; no other file.
* [ ] Phase 3: independent scoped review of the documentation against the code, correct accuracy findings only.
* [ ] Phase 4: changes artifact and state; commit with the repo-local noreply identity and the Copilot trailer; clean ignored files.
* [ ] Phase 5: fetch main and the remote; confirm remote still b82a7c4c; run the full tools/rpi-checks.py --all at the exact clean head in a new external directory with the shared lock and --lock-timeout 14400; official --verify-receipt.
* [ ] Phase 6: only after a verified receipt, normal fast-forward push on top of b82a7c4c (no force needed); refresh the PR body (Refs #444 only); keep draft.

Constraints: no source, test, UI, score, baseline, scorer or workflow edits; local only; no Azure or live action; 8444/8445/8350 untouched; at most 2 correction cycles.
