# Critique: pack citation guard (2026-11-23)

Executed once. Verdict: accept. Findings applied directly:

* Ancestry check must skip, not fail, when git history is shallow or git is absent.
* Resolve by tracked-file path suffix (several cited names have two homes); glob cells via fnmatch.
* Do not pin blob hashes (documents legitimately change).
