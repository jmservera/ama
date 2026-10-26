# Independent review: owner-local resident demo secret helper (issue 462)

* Reviewer: code-review agent, read-only, one original pass, started about 2026-10-26T07:12Z.
* Scope: uncommitted `git diff -- infra` over base `2af9a186` (`credential_arm.py`, new `resident_demo_secrets.py`, new `test_resident_demo_secrets.py`, `infra/README.md`) and the secret-delivery plan.
* Execution: read-only; no tests, Azure or secrets were used by the reviewer.
* Outcome: **Conformant** for this bounded local slice. Not a whole-issue pass, and not an Azure writability or execution approval.

## Reviewer return (unaltered)

No blocking, high, or medium issues. I only read the diff, plan and related scripts and ran nothing, so I haven't confirmed the tests pass.

I checked each of your concerns against the code:

* Secret leakage: Nothing leaks. Secrets reach az only through 0600 temp files inside the 0700 profile directory (credential_arm.py, via tempfile), never through argv or env. The helper's error output is sanitized. The QuietParser at resident_demo_secrets.py:104 never echoes arguments. Azure errors surface only as error.kind or fixed strings (setup-entra.py:63, setup-entra.py:162-181). assert_no_leak also checks that the profile directory is empty afterwards.
* Allowlist: It is not broadened. store() still requires `entra-[a-f0-9]{32}-[a-f0-9]{12}` with a credential parameter, and its tests show it refusing the resident names. store_resident_demo() takes no name or vault input and uses the fixed constants at credential_arm.py:46-48.
* Fail-open: The what-if gate fails closed. It requires Succeeded, every change inside the ama resource group, exactly two actionable changes, set-equality with the two secret IDs, no duplicates, and Create only. The Modify, outside-scope and duplicate cases are tested.
* Expiry and confirmation: Expiry is capped at 12:00Z and rechecked after the typed confirmation. The phrase binds the subscription, vault, both secret names and the expiry.
* TOCTOU: The verifier file is opened once with O_NOFOLLOW, then checked and read through that same descriptor (resident_demo_secrets.py:75-90), so there is no check-then-use gap.
* Employee path: It still works. store() still returns a single URI string, and that is tested.

Low findings

1. infra/scripts/resident_demo_secrets.py:75. os.open on a FIFO with O_RDONLY and no O_NONBLOCK hangs before the fstat check, so a FIFO passed as --verifier-file blocks the helper. It is owner-run and fails safe, so there is no exposure. Adding O_NONBLOCK would fix it.
2. infra/scripts/credential_arm.py (what-if to PUT). A secret created by someone else after the what-if and before the PUT would just get a new version, because the deployment is Incremental. This window is inherent to ARM and the roles are the enforcing control, as the docstring already says. Don't claim atomicity anywhere.
3. infra/tests/test_resident_demo_secrets.py:230-234. The malformed-value assertion is nearly vacuous, because the replace mangles the needle's context. The refusal is still covered by the return code and the empty cli.calls. A plain assertNotIn(bad, self.output) for non-empty values would be stronger.
4. infra/README.md (new paragraph). It says "exactly two" new secrets and that the write is gated. The helper only proves the dry run reads vault metadata, and the what-if runs only under --apply. The wording is accurate, but state it explicitly so nobody reads a dry run as having passed the what-if gate.

Outcome: Conformant. The Low items are optional hardening.

## Routing (recorded by the implementer, after the review)

* No source change was made after the review, so the reviewed hash equals the committed hash. Low findings 1 to 4 are routed to later work (no re-review in this task).
* Finding 2: no atomicity is claimed; Azure RBAC remains the enforcing control.
* Finding 4: the helper docs already state that apply needs separate approval; a dry run is not what-if proof. Recorded as a residual.
