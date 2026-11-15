<!-- markdownlint-disable-file -->
# Changes: issue 441 criterion 9 verification (2026-11-13)

Research: [research](../../research/2026-11-13/441-c9-links-formulas-review-1848-research.md). Plan: [plan](../../plans/2026-11-13/441-c9-links-formulas-review-1848-plan.md). Details: [details](../../details/2026-11-13/441-c9-links-formulas-review-1848-details.md). Critique: [critique](../../reviews/plans/2026-11-13/441-c9-links-formulas-review-1848-plan-critique.md).

## Scope and pin

* Pinned `origin/main` and HEAD: `b630279b411736fb3067fc0747f346baeb81f291` (fetched 2026-11-13). `git diff origin/main HEAD -- docs src` is empty; no dirty file outside `.copilot-tracking/`.
* Verified artifacts: the BRD, PRD, addendum and index; the resident "proposed ADR" is the unregistered proposal under `.copilot-tracking/changes/2026-10-23/resident-portal-requirements-441/` (ADR 0007 on main is the unrelated contractor-intake proposal; no resident ADR ID exists).
* Added files only (no BRD, PRD, ADR, addendum, log, index or issue change): verifier `441-c9-links-formulas-review-1848-verify.py` (SHA-256 `bd8f605a8ca254d4d7538fc6c1eb83cb69836bb4e5b4a412b5b7595f4d06adde`), five fixtures in `441-c9-links-formulas-review-1848-verify-test.py` (pass; ruff check and format clean) and `441-c9-links-formulas-review-1848-report.json` (machine output, `overall_ok: true`). Reproduce from the repository root: `python3 .copilot-tracking/changes/2026-11-13/441-c9-links-formulas-review-1848-verify.py --out report.json`.

## Verification table

| # | Check | Method | Result |
| --- | --- | --- | --- |
| 1 | Freshness | `git fetch`; HEAD equals `origin/main`; docs and src diff; status outside tracking | Pass |
| 2 | SHA-256 of integrated bytes | Table below | Recorded |
| 3 | Original-input custody | 30 declared hashes in the custody JSON (base `140d8f49`) re-hashed against `source-evidence/` copies | 20 matched, 0 mismatched, 10 not archived (tools, state, lint config and the three figures; figures are hashed in row 2 instead). Not-archived originals are unverified, not passed |
| 4 | BRD traceability | Definition rows with "shall": FR-053 to FR-064 (64 FR rows); `ACnnn:` definitions AC-104 to AC-132 plus AC-084 (132 AC) | All present once; no duplicates; base `140d8f49` FR set preserved |
| 5 | PRD traceability | FR-062 to FR-073 (73 FR rows); `\| AC-nnn \| Given` rows AC-111 to AC-140 (130 AC rows in total) | All present once; each AC-111 to AC-140 row names a requirement or goal; the 10 FR-062 to FR-071 matrix rows name BRD FR IDs that all resolve; base FR set preserved |
| 6 | Formulas, BRD 12 derived rows x 3 scenarios | Parsed 13 inputs; unrounded recomputation of W, calls, email, B, G, H, J, S, N, O, F, I compared at table rounding (0.005) | All 36 cells agree; PRD -1.594/14.74/94.333 recomputed exactly; F(U) = 35.4U - 2.96; break-even uptake 8.36%; break-even V 29.90%; F at 25/50/75% uptake is 5.89/14.74/23.59; one-off I (48 base) kept separate from weekly F; "not forecasts" wording present |
| 7 | Policy wording | FR-044, RULE-028, OD-52 to OD-55, log | Per-message named review normative; exception conditional on RULE-028/OD-53; OD-52 to OD-55 visible; no `Closes #441` in the log |
| 8 | Proposed ADR | Proposal text, `docs/adrs`, config and registry | Unregistered and proposed; registry 0001 to 0007, none resident; no `.adr-config.yml` or competing registry; Chrome PNG wording; three figures present |
| 9 | Relative links and heading anchors | 764 relative links over the five documents (24 external, not fetched); GitHub slug and duplicate-suffix rules; code spans and fences skipped | 0 broken in BRD, PRD, addendum and proposal; 2 broken anchors in `docs/reference/README.md` (inherited, below) |
| 10 | Post-#1519 anchors | PRD line 609 and addendum line 1510 | Both resolve to `capstone/history/storage-map-before-reorganization.md#agents-in-the-retrofit-process-2026-10-13` |
| 11 | Markdown lint | `npx markdownlint-cli2` 0.24.1 with the retained 2026-10-23 config on BRD, PRD, addendum, proposal | 6 diagnostics (MD018 x3 in addendum lines 400, 405, 1447; MD056 x3 in PRD lines 856 to 858); identical normalized set to the pre-#1519 parent (`b605f78a3^`); none new |

### Hashes (SHA-256, bytes)

| File | SHA-256 | Bytes |
| --- | --- | --- |
| `docs/brds/agentic-retrofit-programme-brd.md` | `e6dee8e2d56a78115a824b74fc6ff6230640f8bee1922d12cac6371bd929368e` | 302699 |
| `docs/prds/zava-forward-retrofit-programme-demonstrator.md` | `2c7221a04edad4d82706fb3dd537d1c7b9e18f4aaba4e1acc072aa7cab24e058` | 348456 |
| `docs/case_study_48_addendum.md` | `72ee82245d01d67b539ca88c338bab8aea7a5ccfb0ae369050997bc3d34ead05` | 157997 |
| `docs/reference/README.md` | `f290ccc540da4f72c9d1ed8bf9946fb7714b525e13e01dc07a58f0cd82b1678c` | 199513 |
| `resident-service-unregistered-proposal.md` | `45d335fafa4ee346405ac085233ae1e8fb9f092f6b5a61f5da6eb28e7061075a` | 60906 |
| `resident-service-boundary.excalidraw` | `27600e4581f3d7c440adee3d009f2b71099e85991b4dc2dcfa4130003af78d07` | 43454 |
| `resident-service-boundary.svg` | `281d291273e87372eb9efd817c1fe54b4adebb53fbd3a87b46d83c846317bdeb` | 8573 |
| `resident-service-boundary.png` | `118b6cb363ea5686e5f744d5cc3f48b4820d56df14f27825e2d31b3e9f739fcc` | 178186 |

## Inherited-diagnostic comparison

* Same method (this verifier, with anchors) re-run on the pre-#1519 parent blobs: 762 relative links, 4 broken. #1519 repaired two (the PRD:609 and addendum:1510 anchors); two index anchors remain. New since pre-#1519: none.
* Inherited, not owned by #441 and not changed here: `docs/reference/README.md:907` anchor `issue-175-acceptance-audit-2026-10-16` (the target heading is now dated 2026-11-02) and `README.md:1231` anchor `correction-1-and-currency-observed-...-c96a` in the cut-over evidence pack. The 2026-11-01 verifier did not check anchors, so these are findings of the stricter method, not regressions.
* Lint: the six diagnostics are identical on the pre-#1519 parent. Git blame places PRD 856 (the PRD's own AC-104, a different namespace from BRD AC-104) at 2026-10-15 and addendum 400 at 2026-10-13, before the #441 amendment. Not repaired: broad inherited repairs are excluded by the issue.

## Criterion 9 mapping

| Part | Status | Evidence |
| --- | --- | --- |
| Focused Markdown, link, anchor, hash, traceability, formula checks | Recorded, passing at the pinned head | Verification table and report JSON |
| Inherited-diagnostic comparison | Recorded | Section above |
| Exact integrated-byte independent review | Independent `code-review-readiness` of the hashes above and this file; outcome in the review artifact | [review](../../reviews/2026-11-13/441-c9-links-formulas-review-1848-review.md) |
| Required repository publication gates pass before push/PR | Unmet, not run: no complete gate, no hosted CI on a publication head | Focused tier; nothing is pushed |
| No acceptance overclaim | Preserved | Below |

Criterion 9 is not ticked or closed here: publication gates and any push or PR are outside this local lane, and criterion 5 remains owner and Legal gated.

## Not proven

Live resident acceptance, screen-reader or assistive-technology conformance, deployment, spending, final requirements approval, BRD Define and PRD Validate (BLOCKED, quality FAIL), Govern and Finalize (NOT_EVALUATED), ADR ID allocation, OD-52 to OD-55, FR-044/AC-084 requirements-owner disposition, hosted CI for any future head, external links.
