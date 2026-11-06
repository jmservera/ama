<!-- markdownlint-disable-file -->
# Details 004 (activity handoff for #1207), issue 1204

## Phase 1: wording

* Before executing, run `--help` and use `--active`/`--inactive` only when listed.
* Until accepted publication, do not run legacy `--apply`; use the read-only audit, set statuses by hand with readback, report the limitation.
* `--active`: individually confirmed live session or frozen unpublished candidate; positive evidence only, omission is not inactivity.
* `--inactive`: only individually confirmed open issues with no session and no frozen candidate.
* Unknown activity stays explicit (kept In Progress, reported unverified) and is not a global stop.
* Worktree existence, missing upstream or unknown session is not activity or completion proof.
* Board readback, closure review and human gates unchanged.
* Recurring-schedule bullet: delivery prompts carry the handoff; the runtime coordinator replaces the prompt separately.

## Phase 2: checks

Frontmatter unchanged; ASCII only; no new links; earlier C1-C3/M1-M2 clauses and no-bypass wording untouched.
