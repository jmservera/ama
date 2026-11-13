# Plan: 521-azure-preflight-pack-1444

* [ ] 1. Cherry-pick the three package commits (no commit; stage) onto 1ccfae438.
* [ ] 2. Edit infra/README.md Live state check: record the dated 2026-11-13 read-only observation, keep SQL constraint/rows pending.
* [ ] 3. Regenerate cutover-reference-inventory.tsv if offsets shifted; verify cutover_audit --root exits 0.
* [ ] 4. Append dated entry to docs/reference/log.md.
* [ ] 5. ASCII and git diff --check; code-review; single commit with trailer.
