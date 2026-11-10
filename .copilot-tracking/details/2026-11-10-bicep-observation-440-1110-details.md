<!-- markdownlint-disable-file -->
# Plan details: Bicep public-simulation current-main observation (#440, 2026-11-10)

Plan: [plan](../plans/2026-11-10-bicep-observation-440-1110-plan.md).

## Phase 1: pack section

* File `docs/architecture/cutover-evidence-pack.md`, appended at the end, heading `## Bicep public-simulation current-main checkpoint (2026-11-10, Refs #440 #136 #1288)`.
* Subsections: identities and scope; consumed evidence; tree equivalence; Bicep contract trace; evidence classes; findings, owners and gates; recommendation; process record and limits.
* Success: identities equal the research record; counts equal Root raw exits; no claim of a run on `0a6dc0b3f`.

## Phase 2: index and log

* `docs/reference/README.md`: one paragraph appended after the NomUX paragraph, with the section anchor.
* `docs/reference/log.md`: one entry appended after the NomUX entry.

## Phase 3: review and commit

* Added lines scanned for non-ASCII, em dashes and bold-prefix lists; `git diff --check`; anchor present; commit `docs(evidence): ...` with `Refs` only and the Copilot trailer; then witness events and `verify`.
