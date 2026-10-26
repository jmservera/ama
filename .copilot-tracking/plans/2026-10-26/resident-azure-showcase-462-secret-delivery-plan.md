# Issue 462 owner-local secret delivery helper: prospective research and plan

Written 2026-10-26T07:07Z before any source edit. Base head 2af9a186 (11808a01 plus the rubric bot score commit, fast-forwarded; no rebase). Tool authoring only: this is NOT approval to run against Azure, spend, change roles or networks. Frozen candidate 11808a01, all receipts and environments stay untouched.

## Research (read-only, from this repository)

* `infra/scripts/credential_arm.py` already writes one browser credential as a secure ARM deployment: secureString parameter, one `Microsoft.KeyVault/vaults/secrets` resource, no outputs, `az deployment group what-if` first and apply only if it proves exactly one new secret in the selected ama vault, then metadata-only verification (enabled, exp, secretUri). The what-if/deploy bodies pass through `NamedTemporaryFile` in a private 0700 directory outside the repository, deleted on close; nothing goes in argv, env or logs. `store` accepts only `entra-<32hex>-<12hex>` names and must keep doing so for the employee path.
* `vault_id`/`preflight` check the ama resource group, private RBAC vault (public access Disabled) and secret metadata listing, with no data-plane connection.
* `setup-entra.py` supplies `Azure` (CLI runner with sanitized error kinds), `private_path` (refuses symlinks, repo paths, wrong modes) and the isolated tenant profile pattern; `grant-application-admin.py` is the pattern for loading it and for dry-run default and `--apply`.
* `resident_demo_verifier.py` is the offline owner tool. The consumer (`resident_showcase.config_from_env`) needs `ZF_DEMO_PASSWORD_VERIFIER` as a well-formed scrypt verifier (`PasswordVerifier`) and `ZF_DEMO_SESSION_KEY` as base64url of at least 32 bytes.
* Pattern evidence only: no document or test here proves that an ARM secret write succeeds through the private-only vault. The helper tests prove local controls with mocks, not Azure writability.

## Smallest design

1. `credential_arm.store` gains two keyword-only parameters, `name_pattern` (default the existing Entra regex) and `deployment_prefix` (default `entra-`). Defaults keep the employee path byte-identical; its allowlist is not broadened.
2. New `infra/scripts/resident_demo_secrets.py`:
   * Fixed constants: vault `kv-cutovertest-rzsrg`, resource group `ama`, exactly two secret names `resident-demo-password-verifier` and `resident-demo-session-key`, hard maximum expiry `2026-10-26T12:00:00Z`.
   * Inputs: `--subscription`, `--expires` (ISO Z, must be in the future and not after the maximum; else refuse), `--tenant-profile` (private 0700 directory outside the repository, already signed in), optional `--verifier-file` (owner-local regular file, mode 0600, not a symlink, outside the repository, size capped, owned by caller) else a hidden prompt. No secret on argv or env.
   * The verifier is validated with the shared `PasswordVerifier` (no duplicate validator). The session key is `secrets.token_bytes(32)` base64url, generated only at apply time in the owner's process, never printed.
   * Default is a dry run: local validation plus the existing read-only `preflight` (metadata only); sends no secret value to Azure and writes nothing. `--apply` additionally requires an interactive terminal and an exact typed confirmation phrase, and repeats the expiry check just before writing. Each secret is stored through `credential_arm.store`, which runs the what-if gate and refuses anything but one Create of the exact secret.
   * Fails closed: any CredentialError/SetupError becomes a sanitized one-line message and non-zero exit; a partial result (first secret written, second failed) is reported as such, naming the secret, with no values. Never silently succeeds.
   * Documents that apply is not a backdoor: it still needs separate exact write approval, budget clearance (G1) and a proven private write path (G4). Nothing runs at import.
3. Tests `infra/tests/test_resident_demo_secrets.py` using a fake CLI and fake fixtures only; no az, no network, no real values; `secrets.token_bytes` mocked.

## Tests (must fail without the behaviour)

* Fixed names and exact two secrets only; employee `store` still rejects these names and still accepts Entra names.
* Dry run: no write call and no value sent; `--apply` without tty or wrong phrase writes nothing.
* Expiry: missing, past, malformed, after 2026-10-26T12:00Z refused before any call.
* Verifier file: symlink, 0644 mode, directory, repo path, oversize, malformed verifier all refused without echoing content; hidden prompt path accepted with mocked prompt.
* Secret hygiene: fake password-like marker never appears in argv, env snapshot, stdout/stderr or exception text; private body files deleted; error output sanitized.
* What-if boundary: non-single-create what-if refuses before apply; partial failure reported honestly.

## Boundaries and residual risks

* Plaintext verifier and session key exist briefly in the owner's process and in 0700 temp body files in the private tenant profile (existing pattern); no memory/swap/disk-forensics claim.
* ARM deployment history may retain deployment metadata; whether secureString values are excluded from history is Azure's documented behaviour and not proven here.
* The owner needs a login with ARM write rights; the helper grants none.
* No SQL, app, auth, session or domain change; no gate, install, Docker or browser run (disk 6.9 GB, 98%).

## Validation scope

Focused `python -m unittest` on the new test module plus the existing credential tests (`test_staff_azure` credential classes) and ruff on the touched files, using an existing environment without mutating pinned gate venvs. Source change makes every earlier receipt stale for the new head; no gate is run here.

## Independent critique (2026-10-26T07:12Z, one pass, original verdict: Revise; PC-001..003 blocking, PC-004 non-blocking)

* PC-001 accepted. No public regex or prefix parameter. `credential_arm` keeps immutable policies: the Entra regex in `store` and literal constants for the resident pair in a separate `store_resident_demo`; both call one private `_deploy` that takes only already-validated names.
* PC-002 accepted in part. The pair is written by ONE deployment with one what-if that must show exactly two Creates of the two literal secrets, which removes the helper-induced one-secret state but not Azure partial failure. No automatic cleanup or delete path is added, because it would be a new destructive authority; a Modify/NoChange what-if on retry is refused fail-closed and the helper tells the owner to reconcile under a separate exact approval. Recorded as a residual risk, not claimed solved.
* PC-003 accepted in part. Software cannot verify a human or coordinator approval, and a self-attested approval file would be theatre. The earlier claim that apply "cannot be a bypass" is withdrawn. Controls: dry-run default, interactive-only apply, a typed confirmation that must name subscription, vault, both secret names and expiry, mandatory expiry, and Azure RBAC as the actual enforcing control. Separate exact write approval, G1 and G4 are stated as preconditions in the help text and docs, not enforced by code.
* PC-004 accepted. The verifier file is opened once with `O_NOFOLLOW`, then `fstat` on that descriptor checks regular file, owner equals effective uid, mode exactly 0600, size cap, and the same descriptor is read.
