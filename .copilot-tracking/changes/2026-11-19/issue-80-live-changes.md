# Changes: issue 80 live (2026-11-19)

Refs #80. Tier: FOCUSED, docs/tracking only; no `src/` change, so no mypy, ruff or unit tests apply. No Azure resource was created or touched.

| Criterion in #80 | Status | Evidence |
| --- | --- | --- |
| Import shows mapping, conflicts and row-level preview; never changes source | Proven earlier (ticked, not re-opened) | Issue checkbox |
| Every list offers Excel or CSV export; Excel one-way read-only | Proven earlier (ticked, not re-opened) | Issue checkbox |
| Export retains version, source, approval, supersession history | Proven earlier (ticked, not re-opened) | Issue checkbox |
| Owners set the staged transition thresholds (ADR 0001 open item) | Unproven; cannot be proven for the demo | ADR 0001 "Staged transition" still reads "proposed, thresholds to be set by owners"; no targets or N exist; `grep -rn -i threshold src/importer/src` returns nothing on 2026-11-19. Needs named owner decision; an agent-chosen number would not be owner-set. See [2026-11-18 note](../../../docs/reference/research/issue-80-live-transition-thresholds-evidence-2026-11-18.md). |

Result: every remaining criterion needs a human; stopped without source changes.
