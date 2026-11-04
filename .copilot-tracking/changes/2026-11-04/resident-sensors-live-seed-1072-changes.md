<!-- markdownlint-disable-file -->
# Changes: resident sensors live seed (#1072)

* Added research, plan, critique, details, review and state records dated 2026-11-04.
* Added a "Live sensors walk and blocked seed" section to `docs/reference/research/ux/resident-demo-redesign-2026-11-04.md`, updated its row in `docs/reference/README.md`, and appended `docs/reference/log.md`.
* No source, SQL, infrastructure or Azure change. No firewall rule or access setting was created, so no removal was needed. No credential was printed or stored; the walk script and screenshot stayed in `/tmp`.
* Validation: Git diff and Markdown review only; no documentation build or test exists for these files.
* Divergence: the live apply and seed were not performed because the documented route needs access not held; recorded as an owner decision.
