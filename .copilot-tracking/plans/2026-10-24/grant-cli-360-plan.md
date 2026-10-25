# Plan: grant-application-admin CLI body directory (issue 360)

Refs #360 only. Details: ../../details/2026-10-24/grant-cli-360-phase-details.md
* [x] 1 Pass a validated private body directory to `setup.Azure` on `--apply` only.
* [x] 2 Add entrypoint tests with an offline `az` double (real Azure transport): apply writes via a
  temp body that is removed, repeat is idempotent, dry run needs no body directory and issues no
  write, missing write permission refused without a write, failed write refused and no body left,
  unsafe/in-repo profile refused before any az call, no token in output.
* [x] 3 Mutation check: with the fix removed three new tests fail.
* [x] 4 Independent review done (PASS); then full exact-head gate, publish as PR Refs #360.

Critique: not performed before implementation (see research ordering note). The independent review
after implementation is the only independent gate; this is a residual process limitation.
