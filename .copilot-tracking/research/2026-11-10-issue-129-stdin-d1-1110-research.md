<!-- markdownlint-disable-file -->
# Research: issue 129 closed-stdin refusal diagnostic D1

* Branch `feat/demo-constructed-learning-cli-129-1110`; clean head `5cec9663559bebfae3b3a2a7d38fd179b8c84b10`; target main `d52f20a5198de7269f39daf794911545aee01ced`. LOCAL ONLY. Research disposition: `executed`; Planning Readiness: `Ready`.
* Authority: Root authorizes ONE scoped source diagnostic D1 for this newly introduced CLI. One debit; not a whole-issue balance reset or fresh five; no automatic D2/D3.
* Original records are immutable and untouched: `2026-11-10-issue-129-learning-cli-1110-*` (self review R1 stays as written) and the first witness chain (log sha256 `2e1a73fa71f78f3c4f7732e556051fedf482431b80609a43ff6554af2a776874`).

## Evidence

* Independent review (reviewer `dabfdd4e-e835-499f-b8e6-bb1d170f3f90`, read-only, no tests or Git) returned `approve_with_comments` with one Low finding: closed stdin bypasses the refusal handler (`learning_test_bundles.py` lines 317-319). It confirms self-review R1.
* Actual red proof on the original head (external `phase129-stdin-d1-evidence-1110/d1-red-cli.txt`): `python -m zava_forward.core.learning_test_bundles <&-` exits 1, stdout empty, stderr is a traceback ending `AttributeError: 'NoneType' object has no attribute 'isatty'` instead of one `Learning report refused:` line.
* Cause: with descriptor 0 closed, Python sets `sys.stdin` to `None`; `main` calls `sys.stdin.isatty()` inside a handler that catches only `ValueError` and `RecursionError`.

## Conclusion

Smallest fix: an explicit `sys.stdin is None` guard before `isatty`/`buffer`, raising the existing handled `ValueError` with a fixed message. No broader exception catch, no fallback input. Scorer, renderer, comparators, schema, bounds and labels stay unchanged.
