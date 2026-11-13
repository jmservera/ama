---
title: "#176 C2 document-generator provenance plan critique (independent)"
date: 2026-11-13
---

Verdict: REVISE (small, mechanical changes; approach is sound).

## Findings

1. Header-only update: justified and provable.
   * Both committed fixtures round-trip byte-for-byte through `json.dumps(indent=1, sort_keys=True) + "\n"` (checked read-only, no register read). Key insertion plus the same dump therefore yields a minimal diff with one added line per file.
   * `content_sha256` covers only `families`/`cases`, so it cannot change. Proof steps in the plan are adequate: compare JSON minus `generator_revision`, and `git diff --stat` shows +1 line each.
   * Gap: the plan must state that this proves the header only. It does not prove the committed content equals regeneration output from the private register (already recorded as unknown). Keep that disclosure in the change record and PR text.
2. `revision_sources`: sound. `controls` imports `REGISTER`, `_pick_families` and `load_register` from `zf_documents`, so including both files is correct. `source_revision` sorts by basename and requires unique basenames; `zf_documents.py` and `zf_document_controls.py` are unique. The module is path-independent, which suits tests that run from the importer cwd.
   * Risk: the controls revision changes on any `zf_documents.py` edit, and the documents revision on any whitespace edit. A "committed fixture equals current revision" test is therefore a tripwire that forces both headers to be refreshed on every generator edit, including edits that cannot change output. Without the register, a maintainer cannot regenerate, only hand-patch the header. Either accept this and say so in the test docstring and the importer README, or assert only the format (`sha256:` plus 64 hex) and equality with the generator's revision at build time, not with the committed value. Recommended: keep the committed-equality test, since it is the point of #176, and document the refresh step.
   * CRLF/autocrlf could change the revision across checkouts. Check for `.gitattributes` eol handling on `*.py`; if none, note it as a residual risk.
3. Test placement: acceptable, but the details file is self-contradictory (it first rejects, then chooses, the importer file). Rewrite it as a single decision.
   * Control tests in the importer file: workable, because that file already inserts the generator dir into `sys.path` and `zf_document_controls` is importable from there (it imports `zf_documents` by bare name). Read the core fixture by path `src/core/evals/document_control_fixtures.json`. No SQLite is involved.
   * Alternative with better ownership: `src/core/tests/test_synthetic_provenance.py` already references the controls fixture, but it is a core test and may pull in SQLite or other fixtures; the importer placement avoids that. Fine, provided the class name and docstring say it covers the core fixture.
   * Both generators must be imported under distinct module names; `importlib.import_module("zf_document_controls")` is fine because the controls module's `from zf_documents import ...` resolves to the same `gen` module already loaded.
4. Failing-first feasibility: feasible.
   * Tests calling `build()` on the constructed `register()` fail with `KeyError: generator_revision` before the edit, so a real red state exists. Log it.
   * The "reverting the key is detected" replay is just the committed-equality assertion run before the fixture header is added; it should be sequenced explicitly: (a) tests red, (b) generator edit makes build tests green while committed-equality is still red, (c) fixture header update makes it green. The plan merges (b) and (c); split them for a true failing-first record.
   * The controls `build(register, seed)` needs `count` default 120 and a register with at least 120 homes after `_pick_families`; the existing 900-row `register()` helper works.
   * Assert `generator_revision` starts with `sha256:`, has length 71, and is identical across two builds. The "header-only" assertion (content_sha256 equals the hash of families/cases) is better framed as: dropping `generator_revision` leaves the committed dict equal to the previous header set, i.e. `content_sha256` still equals `sha256(json.dumps(families, sort_keys=True))`.
5. Scope and risk gaps.
   * Environment: details specify a venv at `/tmp/zf176c2-venv`. This breaks the never-write-to-/tmp rule and the no-network/no-uv constraint (`pip install -e` may need network for build deps). Required change: use an existing environment, or run with `PYTHONPATH` only if the repository guidance allows it (it says not to add `PYTHONPATH=mvp` workarounds, which concerns a different path). First check whether `zava_forward.core` is already importable (it is not in the default `python3` here: the import check printed no error only if installed; verify) and, if not, use a venv inside the repo working tree outside tracked paths (ignored) with `--no-build-isolation --no-deps`, or state the test as unperformed.
   * `import zava_forward.core.synthetic.provenance` from the generator creates a new runtime dependency on `src/core` being installed when running the generator script. `zf_manifest.py` already does this, so the precedent holds; add one line to the generator docstring, and to `src/importer/README.md` if it documents the generator command.
   * Consumers: other readers of the two fixtures (`src/api/tests/test_document_controls.py`, `src/core/tests/test_synthetic_provenance.py`, importer loaders) read specific keys; an extra header key is low risk. Run the api document-control test and `test_synthetic_provenance` document-control case if they do not start SQLite; otherwise record them as not run.
   * Docs: `docs/reference/research/retrofit-synthetic-data/data-dictionary.md` and the log describe fixture headers. Update the data dictionary header list and append a `docs/reference/log.md` entry (knowledge base convention), or record why not.
   * Revision format: `sha256:` plus 64 hex while other support revisions remain 16 hex. This is a stated non-goal, but note the inconsistency in the change record.
   * Commit: use `gh api user` for the noreply email and include the Co-authored-by trailer; the plan mentions only the noreply email.

## Required changes

1. Replace the `/tmp` venv with a non-/tmp, no-network method, or declare tests unperformed.
2. Split failing-first into red (tests), green build (generator), green committed (fixtures).
3. Resolve the contradictory placement text in the details file.
4. Document the refresh obligation (header must be re-stamped when either generator file changes) and the header-only evidence limit.
5. Add data-dictionary and log updates, and the consumer tests (non-SQLite) to the validation list.
