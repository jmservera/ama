<!-- markdownlint-disable-file -->
# Review: PR 1295 C4 current-main source freshness (2026-11-09)

* Task `pr-1295-c4-current-main-freshness`; one authored self-review after implementation by `hve-core-all:rpi-agent` (Claude Sonnet 5.5). Not independent clearance; independent exact-head review, hosted CI and human approvals remain required.
* Review execution: executed once. Outcome: conformant for the in-scope freshness items; no material finding open.

| Criterion | Status | Evidence |
| --- | --- | --- |
| Ordinary merge of pinned target, no rebase, force or push; both histories preserved; owner ancestry | Met | Merge `2bc249442` clean; `0bcf55da1` and `292d0091a` are ancestors |
| Every refresh justified by a failing check | Met | Pre-refresh failures for architecture, update, Verify, receipt hash and legacy SVG provenance are recorded in the changes record |
| Only actually stale metadata refreshed (resident journey untouched) | Met | Journey `--check` passed before and after; catalog entries for journey, Fabric and Power BI matched |
| Structure, text, geometry and PNG invariance | Met | Masked byte comparison of 8 text artifacts; PNG byte equality |
| No deck, PDF, preview, protected financial or manifest change | Met | `git status` lists no such path; Build PPTX hash equals delivered `949e2077...fa7fca` |
| C3 contracts (13 mapping cases, 55 slides, 108 actions, protected cost) | Met | `Test-DeckInsertion` source and candidate, `Test-CostStatus`, `Verify` all exit 0 |
| Frozen items untouched; no new permission inferred | Met | QX manifest sentence, runbook numbers, protected bytes not edited |
| Live Azure, model, native, AT, notch, rehearsal, human, professional and financial approvals | Unproven by design | Unchanged; no all-55 human acceptance claim |

## Residuals

* Hosted mergeability is unobserved for this head; the earlier CONFLICTING state is at old head `0bcf55da1` and is a post-publication gate.
* `origin/main` is now `df8e858b2` (rubric-only commit after the pinned target); the coordinator should confirm that the reviewer base stays `23e944c1` or accept a trivial merge.
* The simulator job now mounts an admin-written `control.json` in the certificate share (`infra/live-simulator-job.bicep`); the architecture text-equivalent describes the mount without it and contradicts nothing. Whether to mention it is an optional wording follow-up, not a defect.
* The `L69` locator for the simulator in `text-equivalent.md` points to a closing brace; pre-existing, unchanged by main, left alone.
* Owner decisions still frozen: runbook numbers, QX sentence, notch, native, visual, AT, rehearsal and live approvals.
* Budget: C4 is the fourth of five total cycles; one remains, no renewal.
