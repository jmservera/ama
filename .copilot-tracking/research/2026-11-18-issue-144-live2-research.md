# Research: issue 144 live container hosting evidence (2026-11-18)

Unticked criteria: (1) real versioned worker/job images deployed via pipeline; (3) hardening enforced in the deployed app.
Disposition: executed. Planning readiness: pending evidence.

## Findings (executed)

* Unticked: criterion 1 and criterion 3 only. Existing note `docs/reference/research/issue-144-container-hosting-live-evidence-2026-11-18.md` already held a first run; this run re-probed and extended it.
* Evidence is recorded in that note's "Second run" section. Planning readiness: Ready. No source change is warranted: criterion 3 needs a redeploy from current main (deployment change, not authorised); criterion 1 needs a pipeline run requiring protected self-hosted runners.
* Adverse: `ZF_CONTAINER_HARDENING` absent on all deployed apps/jobs; rootfs `overlay rw`; `NoNewPrivs: 0`.

Note: same-named artifacts from an earlier run exist in git and are preserved unmodified; this run uses the `live2` suffix. The state file at the given path was overwritten for this run; the earlier version remains in git history.
