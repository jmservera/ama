<!-- markdownlint-disable-file -->
# Research: #80 browser-built exception-summary CSV, synthetic demo (issue-80-exception-csv-1112)

Research disposition: executed (reading of the reviewed PR1462 contract and of the current source and tests at the pinned base) and reused (the PR1462 universal-inventory research is not repeated). Planning Readiness: Ready.

## Scope and admission

* Worktree issue-80-exception-csv-1112, branch feat/demo-exception-summary-csv-80-1112, base 139176fa0382add781b1830b1ac9db785ed086fe. Local-only frozen candidate: no push, PR, issue or board edit.
* Owner approved on 2026-11-12 "Approve one bounded synthetic-demo implementation" of the reviewed #80 exception-summary CSV proposal. This is one initial bounded candidate. It is not Capacity C6, renewed defaultfive, #135 recovery or an operational export approval. Prior C1-C5 spent counts and adverse evidence are preserved and not reset.
* Eventual PR (not opened here): main, `Refs #80` only. Whole universal export and the staged-Excel thresholds (criterion 4) stay unmet.
* The reviewed contract is the unchanged documentary proposal from PR1462: [research](../../research/2026-11-11/issue-80-exception-contract-2122-research.md), [plan](../../plans/2026-11-11/issue-80-exception-contract-2122-plan.md), [details](../../details/2026-11-11/issue-80-exception-contract-2122-details.md), [critique](../../plans/2026-11-11/issue-80-exception-contract-2122-critique.md), [review](../../reviews/2026-11-11/issue-80-exception-contract-2122-review.md). Those files are not edited by this task.

## Findings at the pinned base

* The register is rendered in `src/api/src/zava_forward/api/web/role-screens.js` (`exceptionRegisterView` at about line 942, `exceptionRegisterPanel` at about line 907). It makes exactly one `GET /api/exceptions` and renders from that response. `exceptionItem` only checks that `id` and `kind` are strings, so the response cannot be trusted for the export without the allowlists in the contract.
* `exceptionKinds` is the closed label vocabulary for six kinds. `owner_role` is `data_steward` or `digital_operator`; `status` is `open` today.
* `exceptionRegisterPanel` already shows an unreadable-entries notice (`data.items.length - items.length`), the empty text, the sources and unrouted lists and the roles-not-named state; these remain the only statement about completeness.
* The repository helper `list_export.safe_cell` (core, Python) fixes the formula prefixes `= + - @ TAB CR`. There is no JavaScript CSV helper and no Blob download precedent in the web layer (`createObjectURL` appears only for photo display in `app.js`). Other exports are server routes with `<a download>`. The browser writer therefore mirrors `safe_cell` for strings and is parity-tested against it.
* `h()` in `app.js` wraps `onclick` in `AsyncAction.handler`, which adds a "working..." status and disables the control during the action. For a synchronous in-memory copy that adds a second live region, so the control attaches a plain `click` listener after creation instead.
* `src/api/tests/test_exception_register_screen.py` `test_no_controls_and_entry_is_a_plain_link` asserts no `button` in the full, empty, denied and entry views. The full fixture includes an unreadable entry (`7`), so it must keep offering no button; the contract requires a new clean populated fixture. The real-browser check `src/api/checks/data_operator_browser_check.py` asserts "no controls in the register panel" on the real populated register; that assertion is directly coupled and must change deliberately to exactly one button, while the check also keeps its no-write and no-model request checks.
* The browser harness (`checks.design_system_browser_check.main`) starts a real loopback server from the worktree `src` paths, so the real script under change is what the browser downloads. The editable pip install points at another checkout, so unit tests that read the web files by path are unaffected; the browser check sets its own `PYTHONPATH`.
* The existing register note and README assertion forbid the phrases "audit trail" and "audit history" in the register (`REGISTER_FORBIDDEN`), so the new note avoids them.

## Evidence limits

* Static and runtime reading of repository files only. No private dataset, cloud, model or spend. No named human, operational or assistive-technology acceptance exists or is claimed.
* Browser-observed requests cannot prove what the server did; the ledger-count claim (O3) is covered at HTTP/Store level only if time allows and is otherwise recorded as not run.

## Follow-ups (current)

* Independent exact-head review before any publication.
* Owner questions P1-P4 from the PR1462 contract remain open (steward and operator naming, retention of a downloaded copy, any real use, Excel thresholds).
