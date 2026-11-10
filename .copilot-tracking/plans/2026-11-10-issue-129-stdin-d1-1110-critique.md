<!-- markdownlint-disable-file -->
# Critique: closed-stdin refusal D1 (single pass, no nested agent)

Executed once by the implementing agent; not independent assessment. Verdict: approve-with-changes.

* C1 applied: close descriptor 0 in the child with `preexec_fn` (shell `<&-` is unavailable through `subprocess`), so the child sees a genuinely closed descriptor rather than a mocked `sys.stdin`. If this proves unusable, record a blocker instead of mocking.
* C2 accepted: only the `None` case is guarded. No broader catch, because the owner forbids it and no evidence shows other stdin failures.
* C3 checked: README already states that refusals print one line and exit 1; no documentation change is required.
