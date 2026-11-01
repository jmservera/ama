# Review: issue 470 faster local gate (2026-11-01)

Review executed once. Outcome: conformant for the delivered slice (evidence-only); issue not closable.

## Acceptance criteria

| Criterion | Status | Evidence |
| --- | --- | --- |
| `--changed` selects groups and records scope | Proven | `changed_groups`, `selection`; `test_changed_selection_mapping_and_closure` passes |
| `--verify-receipt` rejects partial where full required | Proven | `verify(required_scope="full")`; `test_partial_scope_is_rejected_by_default_before_live_probes` passes |
| `--jobs` parallel within single lock and limits | Proven | `worker_limit`, scheduler, `src/README.md` |
| Measured full-run time before and after in the PR | Unmet | No full serial/parallel run; heavy gate not authorised |
| Tests for group selection and receipt scope | Proven | `tools/test_rpi_checks.py` |

## Routed follow-up

Owner-authorised benchmark: `--all --jobs 1` versus `--all --jobs 3` at one clean HEAD, per `src/README.md`, recorded in a PR.
