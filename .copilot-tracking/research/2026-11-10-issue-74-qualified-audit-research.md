# Issue 74 qualified audit supplement: research

Date: 2026-11-10. Task `issue-74-qualified-audit`, parent task `issue-74-main-acceptance-audit` (commit `f6621435387f0d2e6cf5eef2946e7117a17617cf`). Research disposition: executed (reading of existing artifacts and raw logs only; no new runtime check).

## Scope

Documentation qualification only. No source, test, fixture, configuration or dependency change; no fetch, merge, rebase, push or PR. Original evidence, state, self-review and the external handoff are preserved unchanged. Original observations remain attributed to base `c66370042eb08f07839d054433f4483078703cf2` and the original source-qualified synthetic fixture, even if main has advanced. #74 and #73 stay open; criterion 2 is neither ticked nor narrowed.

## Findings

* Start state: HEAD `f6621435387f0d2e6cf5eef2946e7117a17617cf`, tree `d1890b923690f926145e7d01dcf2159870a6297e`, worktree clean, no ignored files.
* Independent reviewer `16d01594-c6d6-4270-846d-52f621953fe8` (readiness findings, one Low): the browser log has 16 PASS lines, not 17.
* Direct count of the original raw `05-browser-check.log` (sha256 `6dfcd77b9d9b4b2b8d614f844e57220ed6f64da9e1f9d512ed39fb49ca79f273`, 18 lines): 16 lines begin `PASS` (lines 1-14, 16, 17), line 15 is `COMPLETE: all checks ran, including axe 4.10.3`, line 18 is `exit=0`. The original "17 PASS" counted the COMPLETE line. Exit 0, no skips, axe 4.10.3 zero violations and no JavaScript errors are unchanged. Core 7 ok and API 3 ok are confirmed in the raw logs.
* Maintained assertions of 17: matrix line 18 and the state `confirmed_decisions` entry; the original external handoff also says 17 and the original review does not state a count. The originals are kept; this supplement corrects by dated addition.
* Root adopted, for planning only, the provisional SYNTHETIC-DEMO outcome interpretation recommended by the Housing Data and Performance Lead (`domain-demo-acceptance-1932.txt`, section 1): a home outcome is a tuple of current lifecycle stage with as-of/source/version, holds and reopening; independent per-measure disposition with evidence, reviewer authority and version, or Unknown; resident handover evidence or Unknown; and intended versus measured performance or Not measured. It is not a customer baseline, approved requirement, observed positive acceptance, resident consent or UI implementation. PRD v0.21.0 is `in-review` and BRD v0.21.0 is `draft`.

## Mapping to original gaps

See the supplement matrix for the table. Gaps G1-G6 are unchanged in status.

## Planning Readiness

Ready.

## Addendum 2026-11-10 (provenance qualification research, task `issue-74-provenance-qualification`)

Disposition: executed (reading only). Input: independent qualification assessment of `cb400d618ec08e1afad9d88a15dee6dcc5e5c2b8` (Medium 1, Low 1, verdict approve with comments; `independent-74-qualified-1983/readiness/readiness-findings.json`).

* Medium: the qualified-audit review says it was executed "after implement-done". The qualified chain (`phase74-qualified-audit-evidence-1110/issue-74/events.jsonl`) lists the review in `dirty_artifacts` at implement-done (seq 5) with the same hash as at review-done (seq 6). The recorded chain does not support the categorical ordering claim. The seven-event verifier and exit 0 do not attest unobserved reasoning or order of work. For contrast, the original chain (f6621435) shows its review first appearing at review-done (seq 6), not at implement-done.
* Medium extension: statements that state validation succeeded as its own call before the first marker (original and qualified handoffs, qualified plan chain) are not established by the retained original logs; the qualified author response disclosed one combined validator plus marker call at implement-start.
* Low: qualified plan Phase 4 is unchecked though its deliverables exist. Only that delivered phase checkbox may be reconciled; no human or PR-review acceptance checkbox is touched.
* Unchanged limits: 16 PASS plus COMPLETE count, c663 attribution, G1-G6 planning mapping, criterion 2 unticked, #74 and #73 open. New execution here does not establish what happened previously.

Planning Readiness: Ready.
