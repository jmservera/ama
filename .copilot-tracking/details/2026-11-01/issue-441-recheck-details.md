<!-- markdownlint-disable-file -->
# Phase details: issue 441 fresh-main recheck

* Phase 1: `verify-441-recheck.py` checks custody hashes (30 files), FR/AC registries against base, policy wording (FR-044, RULE-028, OD-52 to OD-55), the three workload figures, links in the touched documents (resident-related broken links fail, inherited unrelated ones are listed) and the ADR registry state. It writes only `--out`.
* Phase 2: changes file records the head, verifier hash, report hash, overlap table, criterion table and unproven items.
* Phase 3: one `## [2026-11-01] query | ...` entry at the end of `docs/reference/log.md`; no earlier entry edited; no index change because no knowledge-base file is added or moved.
* Phase 4: run verifier, `ruff check`, `ruff format --check`, `git diff --stat`; delegate one independent review of exact bytes.
* Phase 5: `git config --local user.email 8036360+jmservera@users.noreply.github.com`, conventional commit with the Copilot trailer, `git push -u origin HEAD`, `gh pr create --base main`.
