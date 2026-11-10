<!-- markdownlint-disable-file -->
# Changes: discovery CLI checkpoint 440 (2026-11-10)

Task `440-discovery-checkpoint-1110`. Branch `docs/demo-discovery-checkpoint-440-1110` from pinned `origin/main` `0d262beee2dfa6feca27680aa1d596111154c8d9`. No product, test, tool, infra, workflow or policy file changed.

## Files changed

* `docs/architecture/cutover-evidence-pack.md`: appended the section "Discovery CLI feature-increment checkpoint (2026-11-10, Refs #440 #125)". Nothing earlier edited.
* `docs/reference/README.md`: one appended index paragraph pointing at the section.
* `docs/reference/log.md`: one appended entry. Earlier entries untouched.
* New dated RPI records: research, plan, details, critique, this changes record, review, state.

## Execution (actual, tool `date -u` 04:28:51Z to 04:29:23Z)

Environment `/tmp/i440-disc-1110/venv`, Python 3.12.3, editable `src/core` only, import origin under this worktree, `env -i`. Logs outside the repository, 26 files, `SHA256SUMS` `c81aa583a2f706601c97cb2ba639236938842f3fc80abd21c591ea2625ba3675`.

* D1 demo suite exit 0, 14/14. D2 helper suites exit 0, 46/46. D3 version and dependency rule exit 0, 5/5. No skip, no failure.
* D4 CLI twice exit 0, byte-identical 7995 bytes, readback assertions as recorded. D5 no argument 0, extra arguments 2 and 2, unknown subcommand 0.
* D6 poisoned environment exit 0 identical, scratch unchanged, `strace` no connect or socket call and no write-mode open.
* D7 ruff check, ruff format check, mypy exit 0 (tool versions 0.17.3 and 2.4.1 differ from the pins 0.17.1 and 2.4.0). First mypy attempt under `env -i` failed to import; kept as `D7c-first-fault.log`, rerun with the real `HOME`.

## Divergences and amendments

* Research timestamp corrected from a mistaken 04:32Z to 04:28Z (tool clock) before any observation; the research record states the corrected time.
* The review agent (once) found two items, both applied directly: the Records line linked a changes and a review record that did not yet exist (created here), and the D6 "only opens" list omitted the dynamic-linker cache and a FIPS flag probe (reworded).
* The index and log append was done with a short Python write after the evidence pack edit; content was reviewed in the diff.

## Not done

No full or blanket gate, hosted CI read for the exact head, independent exact-head assessment, push, PR, issue write or board write.
