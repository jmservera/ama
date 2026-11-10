<!-- markdownlint-disable-file -->
# Issue 231 positive browser coverage details (2026-11-10)

## P1 Checker edits (`src/api/checks/role_screens_browser_check.py` only)

1. `SCENARIOS["231p"]`: `quality@example.test`, `Technical queue`; exact phrases `Recorded evidence is complete`, `This screen does not approve the stage`, `Signed off on design version 1`, `SYN-STOCK-A v1`, `Reconciled (recorded by a named person)`, `Current design version`, `SYN Designer` and the synthetic person names (finalised from the first rendered run).
2. `SCENARIOS["231qp"]`: `Quality queue`; `Every measure has accepted evidence and no open defect`, `This screen does not record the handover`, `Loft insulation: Accepted`, `QC-LOFT v1`, `SYN Inspector`, `Evidence noted`, `Passed`, `No defect recorded.`
3. New constant `STORY_POSITIVE = ("231p", "231qp")`; add them to `STORY_ACCESSIBLE`. `STORY_231` and `STORY_RESIDENT` unchanged.
4. `positive_technical_quality_data()` private wrapper: `synthetic_data()`; re-run `supplied_resident_fixture` via `runpy` (restores clean documents and the Accepted resident decision); one measure; `hazards = []`; design version 1 with four `Signed off` sign-offs naming `SYN` people; SQ-1 with a terminal `Reconciled` event; one Accepted Loft insulation record with every `QC-LOFT v1` label evidenced, `accepted_by` different from `submitted_by`, and a matching `resident_binding`. A code comment states: synthetic test input, not professional approval, no gate cleared.
5. `check_readonly_accessibility`: insert `elif story in STORY_POSITIVE:` between the resident branch and the existing negative `else`, calling new `check_positive_state`. The existing `else` is untouched.
6. `check_positive_state(page, story)`: exactly one `p.ok[role=status]` in the evidence region, no `.blocked-title`, `Cannot confirm readiness` absent, record-not-approval sentence per story, story-specific source/checklist/person evidence.
7. New `reach_table_regions(page, story, width)` helper (Tab reach of every labelled `div.table-scroll[role=region]` with caption) called at 320 px as well as the existing 1280 px reach; no write controls re-asserted at 320.
8. `run_browser`: positive stories join the scroll-into-view full-text list; take `GET /api/cases/ZF-1` before opening the home and after the checks and require equality; existing generic POST, reflow, reduced-motion, session, error and forbidden-identity checks apply.
9. `__main__`: `positive_technical_quality_data` for `STORY_POSITIVE`.

## P2 Validation

Under `flock -n /tmp/ama-rpi-heavy.lock`, bounded timeouts, external logs in `evidence231/`: browser `231p`, `231qp`, `231`, `231q` with `ZF_AXE_JS` pinned; unit `test_technical_quality_screens`, `test_role_screens`, `test_accessibility_baseline`; `ruff check`, `ruff format --check` (format status compared with the baseline file), `mypy` on the changed file. Negative-control proof: a temporary external copy that points a negative selector at the positive data must fail (not committed).

## P3 Docs and record

`src/api/README.md` paragraph for `231p`/`231qp`. Recipe status: not registered, N/A, re-verified by `git grep` over manifests and workflows.
