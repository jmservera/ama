# Issue 135 C4 independent review and qualification record

Date: 2026-11-10. Scope: metadata only; no source change, no C5. Frozen source head `5a63544c71a3fa61da09094060229061f22119a3`, tree `8245ec2d8c58caafad6b80c00ae83461e34ef933`. The original self-Review (`served-import-refusal-135-c4-review.md`) and all C3 records are preserved unchanged.

## Independent review (coordinator-supplied, same native session eaae, 26-path review)

* Verdict: APPROVE, 0 critical/high/medium/low findings.
* All three original C3 bugs closed for the confirmed paths: failed-transfer persistence (C3-F1), CLI exit-2 contract (C3-F2), stored/shown wording (C3-F3), plus the coupled screen empty-state copy.
* Root re-ran the four original repros (PASS); Core 44 runs with 7 opt-in skips, Importer 79 pass, API 80 pass; Ruff lint/format and mypy PASS for Core (286 files), Importer (12) and API (161).
* Root read the actual disposable MSSQL log: 21 runs, 0 skips, OK.
* Root observer (17 events, zero overflow) supports research, plan, details, changes and critique before the first source edit only.
* Fresh web-design-guidelines one-line check: Pass, using the full current command.md supplied by Root. The initial network retrieval limitation is preserved; the Root-supplied copy resolved it.

Evidence bundle: `independent-135-served-c4-1110/` under the session ROOT (not duplicated here).

## Qualification and limits

* The historical C3 bad order (implementation before research/plan) remains a preserved adverse. It is not retroactively cured and the original C3 code generation is not prospective-order compliant.
* The C4 corrective loop followed genuine forward order and qualifies the final candidate, subject to final metadata assessment and hosted checks.
* Not established: independent CLI-against-MSSQL, assistive-technology acceptance, real appointments or roles, rejected-batch projection, two-file JSON atomicity, whole-135 or parent-73 acceptance.
* Source provenance: the C3 commit 67ad4680 and C4 commit 5a63544c both remain in history.

## Identity check

Source blobs at HEAD match the C4 commit: import_refusals.py 24b32952, sqlstore.py e738b783, exception_register.py b7147f31, importer `__main__.py` 962d75dd, role-screens.js 8b80c934.

Counter: C4/5 used, one remains.
