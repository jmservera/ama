<!-- markdownlint-disable-file -->
# Plan Critique: Issue 440 current-main integration

* Date: 2026-10-25. Executed once, by an independent read-only reviewer (it could not write the file; recorded here verbatim in substance by the parent).
* Verdict: Revise.

## Findings

| ID | Severity | Finding | Disposition |
| --- | --- | --- | --- |
| PC-001 | High | Hard-coded base ea5577b2 conflicts with the plan's stale-base handling; the runner needs --base equal to the current origin/main. | Accepted. The plan now resolves and records the fresh SHA after the final fetch and uses it for --all and --verify-receipt; a moved main routes through merge, conflict verification, cheap checks and the evidence commit before the gate. |
| PC-002 | High | The plan, details, research and critique files are untracked; the runner rejects untracked inputs. P04 did not commit them. | Accepted. P04 now stages and commits all of them with the evidence-pack, log, changes and state updates as one legitimate evidence commit, and requires an empty git status --porcelain --untracked-files=all before launch. Not a receipt-only commit. |
| PC-003 | High | Publication eligibility did not say how RV-003 (attested, unreproduced discovery; human validation) is handled. | Accepted. Per the owner/coordinator instruction, a DRAFT PR is allowed with RV-003, simulated-only behavior evidence and unmet criteria stated as residual work. No Conformant or acceptance claim; the human checkbox stays unchecked. No discovery redo. |
| PC-004 | Medium | The correction procedure applies "only if the gate fails" but P03 may also need a fix. | Accepted. The procedure now covers any P03 or gate failure. |

Merge-commit compatibility with the runner's ancestry and clean checks was confirmed by the reviewer.
