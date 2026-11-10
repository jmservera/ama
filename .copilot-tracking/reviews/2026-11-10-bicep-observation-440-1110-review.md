<!-- markdownlint-disable-file -->
# Review: Bicep public-simulation current-main observation (#440, 2026-11-10)

Single review, executed once after implementation by the author (self-executed, not independent). Changes: [changes](../changes/2026-11-10-bicep-observation-440-1110-changes.md).

## Execution and outcome

* Execution: performed. Boundary: the three docs diff (80 insertions, 0 deletions) plus this observation's RPI records.
* Outcome: conformant with stated limits; no open material finding. Independent exact-head review and hosted checks remain required and are not claimed.

## Checks read

* Identities, counts, exit codes and exclusions in the section match the research record, the Root raw `.exit` files and the live git and gh reads; no command is claimed on `0a6dc0b3f`; Azure observed is none; the PR-head checks are labeled metadata.
* Adverse items stay visible: two lock-busy exit 1 image attempts, the old image as non-proof, three unwaived baseline mypy errors, original C1 to C5 qualifications; image id labeled manifest identity.
* Seal wording keeps the retained-pair versus replaced-pair distinction with no runtime test claimed. The local #89 candidate is stated as not main, with the nomination and UX gate kept distinct from the Bicep wave gate.
* No approval of draft, in-review or proposed documents, no requirement relaxation, no #132 or #133 budget, no closure, no new issue. The NomUX section and CSV-learning record are untouched (insertions only).
* Added lines are ASCII with no em dashes; `git diff --check` clean; heading unique.

## Routed follow-ups (for later user-selected work)

* Independent exact-head readiness of the batch, then applicable hosted CI.
* Root resolution of any append-only conflict preserving both records.
* Separately authorized live inputs for any Azure rollout evidence.
